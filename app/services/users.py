from sqlalchemy import or_
from sqlalchemy.orm import Session

from models.user import UserModel


def list_users(db: Session, search: str | None = None, is_active: bool | None = None):
    """Lấy danh sách user theo từ khóa và trạng thái hoạt động."""
    query = db.query(UserModel)
    if search:
        pattern = f"%{search}%"
        query = query.filter(or_(UserModel.full_name.like(pattern), UserModel.email.like(pattern)))
    if is_active is not None:
        query = query.filter(UserModel.is_active == is_active)
    return query.all()