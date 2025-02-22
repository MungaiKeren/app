from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Recipe, RecipeIngredient, Instruction, User
import schema
from utils import get_current_user

router = APIRouter(
    prefix="/recipes",
    tags=['Recipes']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.RecipeResponse)
def create_recipe(
    recipe: schema.RecipeCreate,
    db: Session = Depends(get_db),
    current_user_email: str = Depends(get_current_user)
):
    # Get user_id from email
    user = db.query(User).filter(User.email == current_user_email).first()
    
    # Create recipe
    db_recipe = Recipe(
        **recipe.dict(exclude={'ingredients', 'instructions'}),
        user_id=user.id
    )
    db.add(db_recipe)
    db.flush()  # This gets us the recipe.id
    
    # Add ingredients
    for ingredient_data in recipe.ingredients:
        recipe_ingredient = RecipeIngredient(
            recipe_id=db_recipe.id,
            **ingredient_data.dict()
        )
        db.add(recipe_ingredient)
    
    # Add instructions
    for instruction_data in recipe.instructions:
        instruction = Instruction(
            recipe_id=db_recipe.id,
            **instruction_data.dict()
        )
        db.add(instruction)
    
    try:
        db.commit()
        db.refresh(db_recipe)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error creating recipe"
        )
    return db_recipe

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
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
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