from fastapi import APIRouter, Depends, HTTPException, status, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import sys
sys.path.append('src')
from src.database import get_db
from src.models import User
from src.schemas.users import UserCreate, UserResponse, UserLogin
from src.crud import get_user_by_email, create_user
from src.auth import get_password_hash, create_access_token

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register new user."""
    existing_user = await get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = get_password_hash(user_data.password)
    user_data_dict = user_data.model_dump()
    user_data_dict["hashed_password"] = hashed_password
    
    user = await create_user(db, user_data_dict)
    return user


@router.post("/login")
async def login_user(
    user_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """Login user and return access token."""
    user = await get_user_by_email(db, user_data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    if not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token = create_access_token(data={"sub": user.id})
    return {"access_token": access_token, "token_type": "bearer"}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password."""
    import os
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_password)
