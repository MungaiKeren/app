from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Ingredient
import schema as schema
from utils import get_current_user

router = APIRouter(
    prefix="/ingredients",
    tags=['Ingredients']
)

@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=schema.IngredientResponse)
def create_ingredient(
    ingredient: schema.IngredientCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    new_ingredient = Ingredient(**ingredient.dict())
    db.add(new_ingredient)
    try:
        db.commit()
        db.refresh(new_ingredient)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ingredient already exists"
        )
    return new_ingredient

@router.get("/", response_model=List[schema.IngredientResponse])
def get_ingredients(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    ingredients = db.query(Ingredient).offset(skip).limit(limit).all()
    return ingredients

@router.get("/{ingredient_id}", response_model=schema.IngredientResponse)
def get_ingredient(
    ingredient_id: int,
    db: Session = Depends(get_db)
):
    ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    if not ingredient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ingredient with id {ingredient_id} not found"
        )
    return ingredient 