from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from db.database import get_db
from schemas.auth import LoginRequest, TokenResponse
from schemas.user import UserCreate, UserResponse
from services.auth import authenticate_user, register_user


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=201)
def register(payload: UserCreate, db: Session = Depends(get_db)):
	"""Đăng ký tài khoản người dùng mới."""
	return register_user(payload, db)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
	"""Đăng nhập và nhận access token."""
	return TokenResponse(access_token=authenticate_user(payload, db))

