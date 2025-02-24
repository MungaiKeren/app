# Recipe API

A FastAPI-based REST API for managing recipes, ingredients, and cooking instructions.

## Project SetUp
Create a parent folder ```recipe-app``` then clone the FAST API app using these commands
``` git clone https://github.com/MungaiKeren/app.git ```


still in the same folder ```recipe-app``` clone the front-end section of this app using this command
``` git clone https://github.com/MungaiKeren/frontend.git ```
The documentation for the api is available on this here[https://github.com/MungaiKeren/frontend]

## Setup API

1. Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment
```source venv/bin/activate```
# On Windows: 
```venv\Scripts\activate```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables in `.env`:
```env
DB_USERNAME=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_NAME=recipe_db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

4. Initialize the database:
```bash
alembic upgrade head
```

5. Seed the database (optional):
```bash
python seeder.py
```

## Database Models

### User
- Email (unique)
- Password (hashed)
- Name
- Created at timestamp
- Relationships: Recipes

### Recipe
- Title
- Description
- Cooking time
- Servings
- User reference
- Created/Updated timestamps
- Relationships: User, Ingredients, Instructions

### Ingredient
- Name
- Unit of measurement

### RecipeIngredient
- Recipe reference
- Ingredient reference
- Quantity
- Notes

### Instruction
- Recipe reference
- Step number
- Description

## API Endpoints

### Authentication
- POST `/auth/login` - User login
- POST `/auth/register` - User registration

### Users
- GET `/users/me` - Get current user
- PUT `/users/me` - Update current user

### Recipes
- GET `/recipes` - List all recipes
- GET `/recipes/my-recipes` - List user's recipes
- GET `/recipes/{recipe_id}` - Get specific recipe
- POST `/recipes` - Create new recipe
- PUT `/recipes/{recipe_id}` - Update recipe
- DELETE `/recipes/{recipe_id}` - Delete recipe

### Ingredients
- GET `/ingredients` - List all ingredients
- GET `/ingredients/{ingredient_id}` - Get specific ingredient
- POST `/ingredients` - Create new ingredient

## Development

### Database Migrations
Create a new migration:
```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback migration:
```bash
alembic downgrade -1
```

### Seeding Data
The seeder creates:
- 4 test users with different cooking styles
- 15 basic ingredients
- 7 recipes distributed among users

Run seeder:
```bash
python seeder.py
```

## Testing
To test the API endpoints using Postman:

1. Register a user or use seeded credentials:
   - Email: john.doe@example.com
   - Password: password123

2. Get JWT token from login endpoint

3. Use Bearer token authentication for protected endpoints

## Technologies Used
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Pydantic
- Python-Jose (JWT)
- Passlib

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## License
MIT License
