from fastapi import FastAPI
from database import engine
from router import posts, users, auth, recipes, ingredients, favorites
from models import User, Recipe, Ingredient, RecipeIngredient, Instruction, Favorite
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Create all tables
User.metadata.create_all(bind=engine)
Recipe.metadata.create_all(bind=engine)
Ingredient.metadata.create_all(bind=engine)
RecipeIngredient.metadata.create_all(bind=engine)
Instruction.metadata.create_all(bind=engine)
Favorite.metadata.create_all(bind=engine)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount all routers under /api prefix
app.include_router(users.router, prefix="/api")
app.include_router(recipes.router, prefix="/api")
app.include_router(ingredients.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(favorites.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to Recipe API"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}