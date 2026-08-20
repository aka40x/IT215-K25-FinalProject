from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from models.research_member import ResearchMemberRoles


class ResearchProjectBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None

class ResearchProjectCreate(ResearchProjectBase):
    pass

class ResearchProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None

class ResearchProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    owner_id: int
    created_at: datetime


class ResearchMemberCreate(BaseModel):
    user_id: int


class ResearchMemberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    project_id: int
    user_id: int
    role: ResearchMemberRoles
    joined_at: datetime