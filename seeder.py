from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import User, Ingredient, Recipe, RecipeIngredient, Instruction
from utils import hash_pass

def seed_ingredients():
    db = SessionLocal()
    try:
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
    
    except Exception as e:
        print(f"Error seeding ingredients: {e}")
        db.rollback()
    finally:
        db.close()

def seed_recipes():
    db = SessionLocal()
    try:
        # Check if recipes already exist
        if db.query(Recipe).first():
            print("Recipes already seeded")
            return

        # Get a user (you'll need at least one user in the database)
        user = db.query(User).first()
        if not user:
            # Create a test user if none exists
            test_user = User(
                email="test@example.com",
                password=hash_pass("password123"),
                name="Test User"
            )
            db.add(test_user)
            db.commit()
            user = test_user

        # Sample recipes
        recipes = [
            {
                "title": "Classic Pancakes",
                "description": "Fluffy and delicious breakfast pancakes",
                "cooking_time": 20,
                "servings": 4,
                "user_id": user.id,
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
                "title": "Simple Pasta Marinara",
                "description": "Quick and easy pasta with tomato sauce",
                "cooking_time": 30,
                "servings": 4,
                "user_id": user.id,
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
                "title": "Chicken Stir Fry",
                "description": "Quick and healthy Asian-inspired stir fry",
                "cooking_time": 25,
                "servings": 4,
                "user_id": user.id,
                "ingredients": [
                    {"ingredient_id": 12, "quantity": 500, "notes": "Sliced"},
                    {"ingredient_id": 13, "quantity": 2, "notes": "Jasmine rice"},
                    {"ingredient_id": 9, "quantity": 3, "notes": "Minced"},
                    {"ingredient_id": 10, "quantity": 1, "notes": "Sliced"},
                    {"ingredient_id": 3, "quantity": 30, "notes": "For cooking"},
                    {"ingredient_id": 1, "quantity": 5, "notes": "To taste"},
                    {"ingredient_id": 2, "quantity": 3, "notes": "To taste"}
                ],
                "instructions": [
                    {"step_number": 1, "description": "Cook rice according to package instructions"},
                    {"step_number": 2, "description": "Heat oil in a large wok or skillet"},
                    {"step_number": 3, "description": "Stir-fry chicken until golden"},
                    {"step_number": 4, "description": "Add garlic and onions, stir-fry until fragrant"},
                    {"step_number": 5, "description": "Season with salt and pepper"},
                    {"step_number": 6, "description": "Serve hot over rice"}
                ]
            },
            {
                "title": "Classic Mac and Cheese",
                "description": "Creamy, comforting macaroni and cheese",
                "cooking_time": 35,
                "servings": 6,
                "user_id": user.id,
                "ingredients": [
                    {"ingredient_id": 14, "quantity": 500, "notes": "Elbow macaroni"},
                    {"ingredient_id": 8, "quantity": 60, "notes": "For roux"},
                    {"ingredient_id": 4, "quantity": 0.5, "notes": "For roux"},
                    {"ingredient_id": 7, "quantity": 750, "notes": "Whole milk"},
                    {"ingredient_id": 15, "quantity": 300, "notes": "Cheddar, grated"},
                    {"ingredient_id": 1, "quantity": 5, "notes": "To taste"},
                    {"ingredient_id": 2, "quantity": 3, "notes": "To taste"}
                ],
                "instructions": [
                    {"step_number": 1, "description": "Cook macaroni according to package instructions"},
                    {"step_number": 2, "description": "Make roux with butter and flour"},
                    {"step_number": 3, "description": "Gradually whisk in milk until smooth"},
                    {"step_number": 4, "description": "Add cheese and stir until melted"},
                    {"step_number": 5, "description": "Season with salt and pepper"},
                    {"step_number": 6, "description": "Combine sauce with cooked macaroni"}
                ]
            },
            {
                "title": "Garlic Butter Rice",
                "description": "Flavorful rice side dish",
                "cooking_time": 25,
                "servings": 4,
                "user_id": user.id,
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
            },
            {
                "title": "Scrambled Eggs",
                "description": "Perfect creamy scrambled eggs",
                "cooking_time": 10,
                "servings": 2,
                "user_id": user.id,
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
            },
            {
                "title": "Tomato Garlic Pasta",
                "description": "Quick and easy vegetarian pasta",
                "cooking_time": 20,
                "servings": 3,
                "user_id": user.id,
                "ingredients": [
                    {"ingredient_id": 14, "quantity": 300, "notes": "Spaghetti"},
                    {"ingredient_id": 11, "quantity": 4, "notes": "Cherry tomatoes"},
                    {"ingredient_id": 9, "quantity": 5, "notes": "Minced"},
                    {"ingredient_id": 3, "quantity": 45, "notes": "Extra virgin"},
                    {"ingredient_id": 15, "quantity": 50, "notes": "Parmesan, grated"},
                    {"ingredient_id": 1, "quantity": 5, "notes": "To taste"},
                    {"ingredient_id": 2, "quantity": 3, "notes": "To taste"}
                ],
                "instructions": [
                    {"step_number": 1, "description": "Cook pasta in salted water"},
                    {"step_number": 2, "description": "Heat oil and sauté garlic until fragrant"},
                    {"step_number": 3, "description": "Add halved tomatoes and cook until soft"},
                    {"step_number": 4, "description": "Toss with cooked pasta"},
                    {"step_number": 5, "description": "Season and top with cheese"}
                ]
            }
        ]

        for recipe_data in recipes:
            # Extract ingredients and instructions
            ingredients = recipe_data.pop('ingredients')
            instructions = recipe_data.pop('instructions')
            
            # Create recipe
            recipe = Recipe(**recipe_data)
            db.add(recipe)
            db.flush()  # Get the recipe ID
            
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
    
    except Exception as e:
        print(f"Error seeding recipes: {e}")
        db.rollback()
    finally:
        db.close()

def reset_database():
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("Database reset complete!")

if __name__ == "__main__":
    print("Starting database reset and seeding...")
    reset_database()
    seed_ingredients()
    seed_recipes()
    print("Seeding completed!") 