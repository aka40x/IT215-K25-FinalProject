from pydantic import BaseModel
from datetime import datetime

from models.research_member import ResearchMemberRoles


class MemberAdd(BaseModel):
    """Dữ liệu xác định người dùng cần thêm vào đề tài."""
    user_id: int


class MemberOut(BaseModel):
    """Dữ liệu thành viên đề tài trả về cho client."""
    user_id: int
    full_name: str
    email: str
    role: ResearchMemberRoles
    joined_at: datetime

    class Config:
        from_attributes = True
