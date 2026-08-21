from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from models.research_member import ResearchMemberRoles


class ResearchProjectBase(BaseModel):
    """Các trường dùng chung của đề tài nghiên cứu."""
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None

class ResearchProjectCreate(ResearchProjectBase):
    """Dữ liệu tạo đề tài nghiên cứu."""
    pass

class ResearchProjectUpdate(BaseModel):
    """Dữ liệu cập nhật một phần đề tài."""
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None

class ResearchProjectResponse(BaseModel):
    """Dữ liệu đề tài trả về cho client."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    owner_id: int
    created_at: datetime


class ResearchMemberCreate(BaseModel):
    """Dữ liệu xác định user cần thêm vào đề tài."""
    user_id: int


class ResearchMemberResponse(BaseModel):
    """Dữ liệu thành viên đề tài trả về cho client."""
    model_config = ConfigDict(from_attributes=True)

    project_id: int
    user_id: int
    role: ResearchMemberRoles
    joined_at: datetime