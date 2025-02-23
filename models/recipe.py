from database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Text, Boolean, Enum, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text
import enum

class CategoryEnum(enum.Enum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    DESSERT = "dessert"
    SNACK = "snack"
    APPETIZER = "appetizer"
    BEVERAGE = "beverage"

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    cooking_time = Column(Integer, nullable=False)  # in minutes
    prep_time = Column(Integer, nullable=True)      # in minutes
    total_time = Column(Integer, nullable=True)     # in minutes
    servings = Column(Integer, nullable=False)
    difficulty = Column(String, nullable=True)      # e.g., "easy", "medium", "hard"
    category = Column(Enum(CategoryEnum), nullable=True)
    cuisine = Column(String, nullable=True)         # e.g., "Italian", "Japanese", "Mexican"
    featured_image = Column(String, nullable=True)  # URL to main recipe image
    additional_images = Column(ARRAY(String), nullable=True)  # Array of image URLs
    calories_per_serving = Column(Integer, nullable=True)
    is_featured = Column(Boolean, default=False)    # For highlighting special recipes
    is_published = Column(Boolean, default=True)    # For draft/published status
    dietary_info = Column(String, nullable=True)    # e.g., "vegetarian", "vegan", "gluten-free"
    notes = Column(Text, nullable=True)            # Additional chef's notes or tips
    source = Column(String, nullable=True)         # Original recipe source if adapted
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), onupdate=text('now()'))

    # Relationships
    user = relationship("User", back_populates="recipes")
    ingredients = relationship("RecipeIngredient", back_populates="recipe", cascade="all, delete-orphan")
    instructions = relationship("Instruction", back_populates="recipe", cascade="all, delete-orphan")
    favorited_by = relationship(
        "User",
        secondary="favorites",
        back_populates="favorite_recipes"
    ) 