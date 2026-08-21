from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from core.exceptions import forbidden, unauthorized
from core.security import decode_access_token
from db.database import get_db
from models.user import UserModel


bearer_scheme = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),db: Session = Depends(get_db),):
    """Giải mã Bearer token và trả về user hiện tại."""
    payload = decode_access_token(credentials.credentials)
    if payload is None:
        raise unauthorized("Token không hợp lệ hoặc đã hết hạn")
    try:
        user_id = int(payload.get("sub"))
    except (TypeError, ValueError):
        raise unauthorized("Token không hợp lệ")

    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise unauthorized("Người dùng không tồn tại")
    if not user.is_active:
        raise forbidden("Tài khoản đã bị khóa")
    return user
