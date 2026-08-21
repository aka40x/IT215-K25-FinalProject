from sqlalchemy.orm import Session

from core.exceptions import bad_request, unauthorized, forbidden
from core.security import create_access_token, hash_password, verify_password
from models.user import UserModel
from schemas.auth import LoginRequest
from schemas.user import UserCreate


def register_user(payload: UserCreate, db: Session):
    """Kiểm tra email và tạo tài khoản mới."""
    existing = db.query(UserModel).filter(UserModel.email == payload.email).first()
    if existing is not None:
        raise bad_request("Email đã được sử dụng")

    user = UserModel(
        email=payload.email,
        password_hash=hash_password(payload.password),
        full_name=payload.full_name,
    )
    db.add(user)
    try:
        db.commit()
        db.refresh(user)
    except Exception:
        db.rollback()
        raise bad_request("Không thể tạo tài khoản")
    return user


def authenticate_user(payload: LoginRequest, db: Session) -> str:
    """Xác thực tài khoản và tạo access token."""
    user = db.query(UserModel).filter(UserModel.email == payload.email).first()
    if user is None or not verify_password(payload.password, user.password_hash):
        raise unauthorized("Email hoặc mật khẩu không đúng")
    if not user.is_active:
        raise forbidden("Tài khoản đã bị khóa")
    return create_access_token(user.id)