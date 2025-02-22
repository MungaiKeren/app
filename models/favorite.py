from database import Base
from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False)

    # Ensure a user can't favorite the same recipe twice
    __table_args__ = (UniqueConstraint('user_id', 'recipe_id', name='unique_user_recipe_favorite'),) 