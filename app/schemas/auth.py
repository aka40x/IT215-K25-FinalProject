from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    """Dữ liệu dùng để đăng nhập."""

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Access token trả về sau khi đăng nhập thành công."""

    access_token: str
    token_type: str = "bearer"