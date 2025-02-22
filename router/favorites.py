from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Favorite, Recipe, User
import schema
from utils import get_current_user

router = APIRouter(
    prefix="/favorites",
    tags=['Favorites']
)

@router.post("/{recipe_id}", status_code=status.HTTP_201_CREATED)
def add_favorite(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user_email: str = Depends(get_current_user)
):
    # Get user
    user = db.query(User).filter(User.email == current_user_email).first()
    
    # Check if recipe exists
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recipe with id {recipe_id} not found"
        )
    
    # Check if already favorited
    existing_favorite = db.query(Favorite).filter(
        Favorite.user_id == user.id,
        Favorite.recipe_id == recipe_id
    ).first()
    
    if existing_favorite:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Recipe already in favorites"
        )
    
    # Create favorite
    favorite = Favorite(user_id=user.id, recipe_id=recipe_id)
    db.add(favorite)
    try:
        db.commit()
        return {"message": "Recipe added to favorites"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not add to favorites"
        )

@router.get("/", response_model=List[schema.RecipeResponse])
def get_favorites(
    db: Session = Depends(get_db),
    current_user_email: str = Depends(get_current_user)
):
    user = db.query(User).filter(User.email == current_user_email).first()
    return user.favorite_recipes

@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_favorite(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user_email: str = Depends(get_current_user)
):
    user = db.query(User).filter(User.email == current_user_email).first()
    
    favorite = db.query(Favorite).filter(
        Favorite.user_id == user.id,
        Favorite.recipe_id == recipe_id
    ).first()
    
    if not favorite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found in favorites"
        )
    
    db.delete(favorite)
    db.commit() 