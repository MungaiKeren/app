from app.database import Base
from sqlalchemy import Column, Integer, ForeignKey, Float, String
from sqlalchemy.orm import relationship

class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"

    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id", ondelete="CASCADE"), primary_key=True)
    quantity = Column(Float, nullable=False)
    notes = Column(String, nullable=True)

    # Relationships
    recipe = relationship("Recipe", back_populates="ingredients")
    ingredient = relationship("Ingredient", back_populates="recipe_ingredients") 