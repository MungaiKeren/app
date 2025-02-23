from pydantic import BaseModel, HttpUrl, constr
from datetime import datetime
from typing import List, Optional
from enum import Enum


class PostBase(BaseModel):
    content: str
    title: str

    class Config:
        from_attributes = True


class CreatePost(PostBase):
    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: str
    password: str
    name: str | None = None


class UserResponse(BaseModel):
    id: int
    email: str
    name: str | None = None
    created_at: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class UserLogin(BaseModel):
    email: str
    password: str


class IngredientBase(BaseModel):
    name: str
    unit: str


class IngredientCreate(IngredientBase):
    pass


class IngredientResponse(IngredientBase):
    id: int

    class Config:
        orm_mode = True


class RecipeIngredientBase(BaseModel):
    ingredient_id: int
    quantity: float
    notes: Optional[str] = None


class RecipeIngredientCreate(RecipeIngredientBase):
    pass


class RecipeIngredientResponse(RecipeIngredientBase):
    ingredient: IngredientResponse

    class Config:
        orm_mode = True


class InstructionBase(BaseModel):
    step_number: int
    description: str


class InstructionCreate(InstructionBase):
    pass


class InstructionResponse(InstructionBase):
    id: int

    class Config:
        orm_mode = True


class CategoryEnum(str, Enum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    DESSERT = "dessert"
    SNACK = "snack"
    APPETIZER = "appetizer"
    BEVERAGE = "beverage"


class RecipeBase(BaseModel):
    title: str
    description: Optional[str] = None
    cooking_time: int
    prep_time: Optional[int] = None
    total_time: Optional[int] = None
    servings: int
    difficulty: Optional[str] = None
    category: Optional[CategoryEnum] = None
    cuisine: Optional[str] = None
    featured_image: Optional[str] = None
    additional_images: Optional[List[str]] = None
    calories_per_serving: Optional[int] = None
    is_featured: Optional[bool] = False
    is_published: Optional[bool] = True
    dietary_info: Optional[str] = None
    notes: Optional[str] = None
    source: Optional[str] = None


class RecipeCreate(BaseModel):
    title: str
    description: str
    cooking_time: int
    prep_time: Optional[int] = None
    total_time: Optional[int] = None
    servings: int
    difficulty: Optional[str] = None
    category: Optional[str] = None
    cuisine: Optional[str] = None
    ingredients: List[RecipeIngredientCreate]
    instructions: List[InstructionCreate]
    featured_image: Optional[HttpUrl] = None
    additional_images: Optional[List[HttpUrl]] = None


class RecipeResponse(RecipeBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    ingredients: List[RecipeIngredientResponse]
    instructions: List[InstructionResponse]
    user: UserResponse

    class Config:
        from_attributes = True