from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
from uuid import uuid4
import shutil

load_dotenv()

# JWT Settings
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def hash_pass(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return email
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def copy_sample_image(image_name: str) -> str:
    """Copy a sample image from assets to uploads directory"""
    UPLOAD_DIR = "uploads/recipes"
    ASSETS_DIR = "assets/sample_images"
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    # Generate unique filename while keeping the extension
    file_extension = os.path.splitext(image_name)[1].lower()
    unique_filename = f"{uuid4()}{file_extension}"
    
    source_path = os.path.join(ASSETS_DIR, image_name)
    destination_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    shutil.copy2(source_path, destination_path)
    return destination_path

def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_token(token)