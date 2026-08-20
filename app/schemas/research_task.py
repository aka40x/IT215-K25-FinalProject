from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from models.research_task import TaskPriority, TaskStatus


class ResearchTaskBase(BaseModel):
    title: str = Field( min_length=1, max_length=255)
    description: str | None = None
    assignee_id: int | None = None
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: datetime | None = None

class ResearchTaskCreate(ResearchTaskBase):
    pass

class ResearchTaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    assignee_id: int | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    due_date: datetime | None = None

class ResearchTaskResponse(BaseModel):
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
    
    