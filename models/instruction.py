from database import Base
from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

class Instruction(Base):
    __tablename__ = "instructions"

    id = Column(Integer, primary_key=True, nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False)
    step_number = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)

    # Relationship
    recipe = relationship("Recipe", back_populates="instructions") 