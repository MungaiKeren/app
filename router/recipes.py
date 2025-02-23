from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import Recipe, RecipeIngredient, Instruction, User, Ingredient
import schema as schema
from utils import get_current_user
import shutil
import os
from uuid import uuid4
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError

router = APIRouter(
    prefix="/recipes",
    tags=['Recipes']
)

@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=schema.RecipeResponse)
async def create_recipe(
    recipe: schema.RecipeCreate,
    db: Session = Depends(get_db),
    current_user_email: str = Depends(get_current_user)
):
    try:
        # Get user_id from email
        user = db.query(User).filter(User.email == current_user_email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Convert recipe data to dict and handle HttpUrl fields
        recipe_data = recipe.dict(exclude={'ingredients', 'instructions'})
        
        # Convert HttpUrl to string for featured_image
        if recipe_data.get('featured_image'):
            recipe_data['featured_image'] = str(recipe_data['featured_image'])
        
        # Convert HttpUrl list to string list for additional_images
        if recipe_data.get('additional_images'):
            recipe_data['additional_images'] = [str(url) for url in recipe_data['additional_images']]
        
        # Create recipe
        db_recipe = Recipe(
            **recipe_data,
            user_id=user.id
        )
        db.add(db_recipe)
        db.flush()  # This gets us the recipe.id
        
        # Add ingredients through the join table
        for ingredient_data in recipe.ingredients:
            # Verify ingredient exists
            ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_data.ingredient_id).first()
            if not ingredient:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Ingredient with id {ingredient_data.ingredient_id} not found"
                )
            
            # Create recipe_ingredient association
            recipe_ingredient = RecipeIngredient(
                recipe_id=db_recipe.id,
                ingredient_id=ingredient_data.ingredient_id,
                quantity=ingredient_data.quantity,
                notes=ingredient_data.notes
            )
            db.add(recipe_ingredient)
        
        # Add instructions
        for instruction_data in recipe.instructions:
            instruction = Instruction(
                recipe_id=db_recipe.id,
                **instruction_data.dict()
            )
            db.add(instruction)
        
        db.commit()
        db.refresh(db_recipe)
        return db_recipe

    except HTTPException as he:
        db.rollback()
        raise he
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "msg": "Database error while creating recipe",
                "error": str(e)
            }
        )
    except ValidationError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "msg": "Validation error",
                "errors": e.errors()
            }
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "msg": "An unexpected error occurred",
                "error": str(e)
            }
        )

@router.get("/", response_model=List[schema.RecipeResponse])
def get_recipes(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10
):
    recipes = db.query(Recipe).offset(skip).limit(limit).all()
    return recipes

@router.get("/my-recipes", response_model=List[schema.RecipeResponse])
def get_user_recipes(
    db: Session = Depends(get_db),
    current_user_email: str = Depends(get_current_user)
):
    user = db.query(User).filter(User.email == current_user_email).first()
    recipes = db.query(Recipe).filter(Recipe.user_id == user.id).all()
    return recipes

@router.get("/{recipe_id}", response_model=schema.RecipeResponse)
def get_recipe(
    recipe_id: int,
    db: Session = Depends(get_db)
):
    # Load recipe with relationships (ingredients and instructions)
    recipe = db.query(Recipe)\
        .filter(Recipe.id == recipe_id)\
        .first()
    
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recipe with id {recipe_id} not found"
        )
    return recipe

@router.put("/{recipe_id}", response_model=schema.RecipeResponse)
def update_recipe(
    recipe_id: int,
    recipe_update: schema.RecipeCreate,
    db: Session = Depends(get_db),
    current_user_email: str = Depends(get_current_user)
):
    # Get user
    user = db.query(User).filter(User.email == current_user_email).first()
    
    # Check recipe exists and belongs to user
    recipe_query = db.query(Recipe).filter(Recipe.id == recipe_id)
    recipe = recipe_query.first()
    
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recipe with id {recipe_id} not found"
        )
    
    if recipe.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action"
        )
    
    # Update recipe basic info
    recipe_query.update(recipe_update.dict(exclude={'ingredients', 'instructions'}))
    
    # Delete existing ingredients and instructions
    db.query(RecipeIngredient).filter(RecipeIngredient.recipe_id == recipe_id).delete()
    db.query(Instruction).filter(Instruction.recipe_id == recipe_id).delete()
    
    # Add new ingredients
    for ingredient_data in recipe_update.ingredients:
        recipe_ingredient = RecipeIngredient(
            recipe_id=recipe_id,
            **ingredient_data.dict()
        )
        db.add(recipe_ingredient)
    
    # Add new instructions
    for instruction_data in recipe_update.instructions:
        instruction = Instruction(
            recipe_id=recipe_id,
            **instruction_data.dict()
        )
        db.add(instruction)
    
    db.commit()
    return recipe_query.first()

@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user_email: str = Depends(get_current_user)
):
    # Get user
    user = db.query(User).filter(User.email == current_user_email).first()
    
    # Check recipe exists and belongs to user
    recipe_query = db.query(Recipe).filter(Recipe.id == recipe_id)
    recipe = recipe_query.first()
    
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recipe with id {recipe_id} not found"
        )
    
    if recipe.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action"
        )
    
    recipe_query.delete(synchronize_session=False)
    db.commit() 

async def save_image(image: UploadFile) -> str:
    # Create uploads directory if it doesn't exist
    UPLOAD_DIR = "uploads/recipes"
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    # Generate unique filename
    file_extension = os.path.splitext(image.filename)[1].lower()
    unique_filename = f"{uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # Save the file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    
    return file_path 