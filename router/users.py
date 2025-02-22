from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import schema
from user import User
from utils import hash_pass

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.UserResponse)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    # Hash the password
    hashed_password = hash_pass(user.password)
    user.password = hashed_password
    
    # Create new user
    new_user = User(**user.dict())
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                          detail="Email already registered")
    return new_user

@router.get("/", response_model=List[schema.UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@router.get("/{id}", response_model=schema.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail=f"User with id: {id} does not exist")
    return user

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    user_query = db.query(User).filter(User.id == id)
    user = user_query.first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail=f"User with id: {id} does not exist")
    
    user_query.delete(synchronize_session=False)
    db.commit()

@router.put("/{id}", response_model=schema.UserResponse)
def update_user(id: int, updated_user: schema.UserCreate, db: Session = Depends(get_db)):
    user_query = db.query(User).filter(User.id == id)
    user = user_query.first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail=f"User with id: {id} does not exist")
    
    update_data = updated_user.dict()
    update_data["password"] = hash_pass(update_data["password"])
    
    user_query.update(update_data, synchronize_session=False)
    db.commit()
    
    return user_query.first() 