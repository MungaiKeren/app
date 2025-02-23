from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal
from models import User, Ingredient, Recipe, RecipeIngredient, Instruction, CategoryEnum
from utils import hash_pass, copy_sample_image
import shutil
import os
from pathlib import Path
import json

def reset_database():
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("Database reset complete!")

def seed_users(db: Session):
    # Check if users already exist
    if db.query(User).first():
        print("Users already seeded")
        return []

    # Create multiple users
    users = [
        {
            "email": "john.doe@example.com",
            "password": hash_pass("password123"),
            "name": "John Doe"
        },
        {
            "email": "mary.smith@example.com",
            "password": hash_pass("password123"),
            "name": "Mary Smith"
        },
        {
            "email": "chef.ramsey@example.com",
            "password": hash_pass("password123"),
            "name": "Gordon Ramsey"
        },
        {
            "email": "julia.child@example.com",
            "password": hash_pass("password123"),
            "name": "Julia Child"
        }
    ]

    created_users = []
    for user_data in users:
        user = User(**user_data)
        db.add(user)
        created_users.append(user)
    
    db.commit()
    print("Users seeded successfully")
    return created_users

def seed_ingredients(db: Session):
    # Check if ingredients already exist
    if db.query(Ingredient).first():
        print("Ingredients already seeded")
        return

    # Basic ingredients
    ingredients = [
        {"name": "Salt", "unit": "grams"},
        {"name": "Black Pepper", "unit": "grams"},
        {"name": "Olive Oil", "unit": "ml"},
        {"name": "Flour", "unit": "cups"},
        {"name": "Sugar", "unit": "grams"},
        {"name": "Eggs", "unit": "pieces"},
        {"name": "Milk", "unit": "ml"},
        {"name": "Butter", "unit": "grams"},
        {"name": "Garlic", "unit": "cloves"},
        {"name": "Onion", "unit": "pieces"},
        {"name": "Tomatoes", "unit": "pieces"},
        {"name": "Chicken Breast", "unit": "grams"},
        {"name": "Rice", "unit": "cups"},
        {"name": "Pasta", "unit": "grams"},
        {"name": "Cheese", "unit": "grams"}
    ]

    for ingredient_data in ingredients:
        ingredient = Ingredient(**ingredient_data)
        db.add(ingredient)
    
    db.commit()
    print("Ingredients seeded successfully")

def setup_sample_images():
    """Return default image URLs for seeding"""
    return {
        "placeholder": "https://unsplash.com/photos/four-assorted-dishes-on-wooden-surface-I2uJU-5ZIGI",
        "food": "https://unsplash.com/photos/grilled-fish-cooked-vegetables-and-fork-on-plate-bpPTlXWTOvg",
        "breakfast": "https://unsplash.com/photos/round-white-ceramic-plate-filled-with-waffle-hrlvr2ZlUNk",
        "dinner": "https://unsplash.com/photos/white-and-green-ceramic-plates-on-brown-wooden-dining-table-fb0_wj2MZk4"
    }

def seed_recipes(db: Session, users: list[User]):
    if db.query(Recipe).first():
        print("Recipes already seeded")
        return

    # Get placeholder images
    images = setup_sample_images()
    
    recipes = {
        # John Doe - Simple home cooking
        users[0].id: [
            {
                "title": "Classic Pancakes",
                "description": "Fluffy and delicious breakfast pancakes",
                "cooking_time": 20,
                "prep_time": 10,
                "total_time": 30,
                "servings": 4,
                "difficulty": "easy",
                "category": CategoryEnum.BREAKFAST,
                "cuisine": "American",
                "featured_image": images["breakfast"],
                "additional_images": json.dumps([images["food"]]),
                "calories_per_serving": 250,
                "is_featured": True,
                "dietary_info": "vegetarian",
                "notes": "For extra fluffy pancakes, don't overmix the batter",
                "source": "Family recipe",
                "ingredients": [
                    {"ingredient_id": 4, "quantity": 1.5, "notes": "All-purpose flour"},
                    {"ingredient_id": 5, "quantity": 50, "notes": "Granulated sugar"},
                    {"ingredient_id": 1, "quantity": 5, "notes": "Just a pinch"},
                    {"ingredient_id": 7, "quantity": 250, "notes": "Room temperature"},
                    {"ingredient_id": 6, "quantity": 2, "notes": "Large eggs"},
                    {"ingredient_id": 8, "quantity": 30, "notes": "Melted"}
                ],
                "instructions": [
                    {"step_number": 1, "description": "Mix flour, sugar, and salt in a bowl"},
                    {"step_number": 2, "description": "In another bowl, whisk milk, eggs, and melted butter"},
                    {"step_number": 3, "description": "Combine wet and dry ingredients until just mixed"},
                    {"step_number": 4, "description": "Cook on a hot griddle until bubbles form"},
                    {"step_number": 5, "description": "Flip and cook until golden brown"}
                ]
            },
            {
                "title": "Scrambled Eggs",
                "description": "Perfect creamy scrambled eggs",
                "cooking_time": 10,
                "prep_time": 5,
                "total_time": 15,
                "servings": 2,
                "difficulty": "easy",
                "category": CategoryEnum.BREAKFAST,
                "cuisine": "International",
                "featured_image": images["breakfast"],
                "calories_per_serving": 180,
                "is_featured": False,
                "dietary_info": "gluten-free",
                "notes": "Low heat is key for creamy eggs",
                "ingredients": [
                    {"ingredient_id": 6, "quantity": 4, "notes": "Fresh eggs"},
                    {"ingredient_id": 8, "quantity": 30, "notes": "For cooking"},
                    {"ingredient_id": 7, "quantity": 30, "notes": "A splash"},
                    {"ingredient_id": 1, "quantity": 3, "notes": "To taste"},
                    {"ingredient_id": 2, "quantity": 2, "notes": "To taste"}
                ],
                "instructions": [
                    {"step_number": 1, "description": "Whisk eggs with milk"},
                    {"step_number": 2, "description": "Melt butter in non-stick pan over medium heat"},
                    {"step_number": 3, "description": "Pour in eggs and stir gently"},
                    {"step_number": 4, "description": "Cook until just set but still creamy"},
                    {"step_number": 5, "description": "Season with salt and pepper"}
                ]
            }
        ],
        # Mary Smith - Quick and easy meals
        users[1].id: [
            {
                "title": "Simple Pasta Marinara",
                "description": "Quick and easy pasta with tomato sauce",
                "cooking_time": 30,
                "prep_time": 10,
                "total_time": 40,
                "servings": 4,
                "difficulty": "easy",
                "category": CategoryEnum.DINNER,
                "cuisine": "Italian",
                "featured_image": images["dinner"],
                "calories_per_serving": 380,
                "is_featured": True,
                "dietary_info": "vegetarian",
                "notes": "Use San Marzano tomatoes for best results",
                "source": "Italian cookbook",
                "ingredients": [
                    {"ingredient_id": 14, "quantity": 500, "notes": "Spaghetti"},
                    {"ingredient_id": 3, "quantity": 30, "notes": "Extra virgin"},
                    {"ingredient_id": 9, "quantity": 4, "notes": "Minced"},
                    {"ingredient_id": 10, "quantity": 1, "notes": "Finely chopped"},
                    {"ingredient_id": 11, "quantity": 4, "notes": "Ripe, crushed"},
                    {"ingredient_id": 1, "quantity": 5, "notes": "To taste"},
                    {"ingredient_id": 2, "quantity": 3, "notes": "Freshly ground"}
                ],
                "instructions": [
                    {"step_number": 1, "description": "Boil pasta according to package instructions"},
                    {"step_number": 2, "description": "Heat oil and sauté garlic and onions"},
                    {"step_number": 3, "description": "Add tomatoes and simmer for 15 minutes"},
                    {"step_number": 4, "description": "Season with salt and pepper"},
                    {"step_number": 5, "description": "Combine sauce with cooked pasta"}
                ]
            },
            {
                "title": "Garlic Butter Rice",
                "description": "Flavorful rice side dish",
                "cooking_time": 25,
                "servings": 4,
                "ingredients": [
                    {"ingredient_id": 13, "quantity": 2, "notes": "Long grain rice"},
                    {"ingredient_id": 8, "quantity": 50, "notes": "Unsalted"},
                    {"ingredient_id": 9, "quantity": 6, "notes": "Minced"},
                    {"ingredient_id": 1, "quantity": 5, "notes": "To taste"},
                    {"ingredient_id": 2, "quantity": 3, "notes": "To taste"}
                ],
                "instructions": [
                    {"step_number": 1, "description": "Rinse rice until water runs clear"},
                    {"step_number": 2, "description": "Cook rice in rice cooker or pot"},
                    {"step_number": 3, "description": "Melt butter in a pan and sauté garlic"},
                    {"step_number": 4, "description": "Fold garlic butter into cooked rice"},
                    {"step_number": 5, "description": "Season with salt and pepper"}
                ]
            }
        ],
        # Gordon Ramsey - Professional recipes
        users[2].id: [
            {
                "title": "Gourmet Mac and Cheese",
                "description": "Restaurant-style creamy macaroni and cheese",
                "cooking_time": 35,
                "servings": 6,
                "ingredients": [
                    {"ingredient_id": 14, "quantity": 500, "notes": "Artisanal elbow macaroni"},
                    {"ingredient_id": 8, "quantity": 60, "notes": "European-style butter"},
                    {"ingredient_id": 4, "quantity": 0.5, "notes": "For perfect roux"},
                    {"ingredient_id": 7, "quantity": 750, "notes": "Full-fat milk"},
                    {"ingredient_id": 15, "quantity": 300, "notes": "Aged cheddar"},
                    {"ingredient_id": 1, "quantity": 5, "notes": "Sea salt"},
                    {"ingredient_id": 2, "quantity": 3, "notes": "Freshly cracked"}
                ],
                "instructions": [
                    {"step_number": 1, "description": "Cook pasta in heavily salted water until al dente"},
                    {"step_number": 2, "description": "Create a blonde roux with butter and flour"},
                    {"step_number": 3, "description": "Gradually incorporate warm milk while whisking"},
                    {"step_number": 4, "description": "Fold in aged cheddar until perfectly smooth"},
                    {"step_number": 5, "description": "Season with sea salt and fresh pepper"},
                    {"step_number": 6, "description": "Combine with pasta and finish under the broiler"}
                ]
            }
        ],
        # Julia Child - Classic cooking
        users[3].id: [
            {
                "title": "Classic Chicken Stir Fry",
                "description": "Traditional Asian-inspired stir fry",
                "cooking_time": 25,
                "servings": 4,
                "ingredients": [
                    {"ingredient_id": 12, "quantity": 500, "notes": "Thinly sliced"},
                    {"ingredient_id": 13, "quantity": 2, "notes": "Jasmine rice"},
                    {"ingredient_id": 9, "quantity": 3, "notes": "Fresh minced"},
                    {"ingredient_id": 10, "quantity": 1, "notes": "Julienned"},
                    {"ingredient_id": 3, "quantity": 30, "notes": "High quality"},
                    {"ingredient_id": 1, "quantity": 5, "notes": "To taste"},
                    {"ingredient_id": 2, "quantity": 3, "notes": "Freshly ground"}
                ],
                "instructions": [
                    {"step_number": 1, "description": "Prepare rice using the absorption method"},
                    {"step_number": 2, "description": "Heat wok until smoking"},
                    {"step_number": 3, "description": "Stir-fry chicken in batches until golden"},
                    {"step_number": 4, "description": "Add aromatics and vegetables"},
                    {"step_number": 5, "description": "Season and serve immediately"}
                ]
            },
            {
                "title": "Tomato Garlic Pasta",
                "description": "Mediterranean-style pasta dish",
                "cooking_time": 20,
                "servings": 3,
                "ingredients": [
                    {"ingredient_id": 14, "quantity": 300, "notes": "Fresh pasta"},
                    {"ingredient_id": 11, "quantity": 4, "notes": "Vine-ripened"},
                    {"ingredient_id": 9, "quantity": 5, "notes": "Fresh cloves"},
                    {"ingredient_id": 3, "quantity": 45, "notes": "First cold press"},
                    {"ingredient_id": 15, "quantity": 50, "notes": "Aged Parmigiano"},
                    {"ingredient_id": 1, "quantity": 5, "notes": "Sea salt"},
                    {"ingredient_id": 2, "quantity": 3, "notes": "Fresh ground"}
                ],
                "instructions": [
                    {"step_number": 1, "description": "Cook pasta in salted water until al dente"},
                    {"step_number": 2, "description": "Prepare garlic and tomato sauce"},
                    {"step_number": 3, "description": "Combine pasta with sauce"},
                    {"step_number": 4, "description": "Finish with olive oil and cheese"},
                    {"step_number": 5, "description": "Garnish with fresh herbs"}
                ]
            }
        ]
    }

    # Create recipes for each user
    for user_id, user_recipes in recipes.items():
        for recipe_data in user_recipes:
            # Convert additional images list to JSON string if it exists
            if 'additional_images' in recipe_data:
                recipe_data['additional_images'] = json.dumps(recipe_data['additional_images'])
            
            # Extract ingredients and instructions
            ingredients = recipe_data.pop('ingredients')
            instructions = recipe_data.pop('instructions')
            
            # Create recipe
            recipe = Recipe(**recipe_data, user_id=user_id)
            db.add(recipe)
            db.flush()
            
            # Add ingredients
            for ing_data in ingredients:
                recipe_ingredient = RecipeIngredient(recipe_id=recipe.id, **ing_data)
                db.add(recipe_ingredient)
            
            # Add instructions
            for inst_data in instructions:
                instruction = Instruction(recipe_id=recipe.id, **inst_data)
                db.add(instruction)
    
    db.commit()
    print("Recipes seeded successfully")

if __name__ == "__main__":
    print("Starting database reset and seeding...")
    reset_database()
    setup_sample_images()
    
    # Use a single database session for all operations
    db = SessionLocal()
    try:
        users = seed_users(db)
        seed_ingredients(db)
        seed_recipes(db, users)
        print("Seeding completed!")
    except Exception as e:
        print(f"Error during seeding: {e}")
        db.rollback()
    finally:
        db.close() 