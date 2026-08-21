from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from models.user import UserRoles


class UserBase(BaseModel):
    """Các trường dùng chung của dữ liệu người dùng."""
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    """Dữ liệu tạo tài khoản mới."""
    password: str

class UserUpdate(BaseModel):
    """Dữ liệu cập nhật một phần tài khoản."""
    full_name: str | None = None
    is_active: bool | None = None
    # password: str | None = None

class UserResponse(BaseModel):
    """Dữ liệu user trả về cho client, không gồm mật khẩu."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    full_name: str
    role: UserRoles
    is_active: bool
    created_at: datetime
    
""" Cần note lại phần nào cần làm gì để sau còn sửa được """