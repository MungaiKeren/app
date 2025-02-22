from fastapi import FastAPI
from database import engine
from router import posts, users, auth, recipes, ingredients, favorites
from models import User, Recipe, Ingredient, RecipeIngredient, Instruction

app = FastAPI()

# Create all tables
User.metadata.create_all(bind=engine)
Recipe.metadata.create_all(bind=engine)
Ingredient.metadata.create_all(bind=engine)
RecipeIngredient.metadata.create_all(bind=engine)
Instruction.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(recipes.router)
app.include_router(ingredients.router)
app.include_router(favorites.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Recipe API"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}