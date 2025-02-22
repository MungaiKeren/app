from database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    unit = Column(String, nullable=False)

    # Relationship
    recipe_ingredients = relationship("RecipeIngredient", back_populates="ingredient") 