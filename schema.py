from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class PostBase(BaseModel):
    content: str
    title: str

    class Config:
        orm_mode = True


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


class RecipeBase(BaseModel):
    title: str
    description: Optional[str] = None
    cooking_time: int
    servings: int


class RecipeCreate(RecipeBase):
    ingredients: List[RecipeIngredientCreate]
    instructions: List[InstructionCreate]


class RecipeResponse(RecipeBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    ingredients: List[RecipeIngredientResponse]
    instructions: List[InstructionResponse]
    user: UserResponse

    class Config:
        orm_mode = True