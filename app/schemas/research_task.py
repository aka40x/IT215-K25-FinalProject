from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from models.research_task import TaskPriority, TaskStatus


class ResearchTaskBase(BaseModel):
    """Các trường dùng chung của nhiệm vụ nghiên cứu."""
    title: str = Field( min_length=1, max_length=255)
    description: str | None = None
    assignee_id: int | None = None
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: datetime | None = None

class ResearchTaskCreate(ResearchTaskBase):
    """Dữ liệu tạo nhiệm vụ nghiên cứu."""
    pass

class ResearchTaskUpdate(BaseModel):
    """Dữ liệu cập nhật một phần nhiệm vụ."""
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    assignee_id: int | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    due_date: datetime | None = None

class ResearchTaskResponse(BaseModel):
    """Dữ liệu nhiệm vụ trả về cho client."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    title: str
    description: str | None
    assignee_id: int | None
    status: TaskStatus
    priority: TaskPriority
    due_date: datetime | None
    created_at: datetime
    
    