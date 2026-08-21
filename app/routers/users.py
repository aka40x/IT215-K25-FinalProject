from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from db.database import get_db
from dependencies.auth import get_current_user
from dependencies.roles import require_admin
from models.user import UserModel
from schemas.user import UserResponse
from services.users import list_users


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: UserModel = Depends(get_current_user)):
    """Lấy thông tin tài khoản hiện tại."""
    return current_user


@router.get("", response_model=list[UserResponse])
def get_users(
    search: str | None = Query(default=None),
    is_active: bool | None = Query(default=None),
    db: Session = Depends(get_db),
    _: UserModel = Depends(require_admin),
):
    """Admin lấy danh sách user theo bộ lọc."""
    return list_users(db, search=search, is_active=is_active)