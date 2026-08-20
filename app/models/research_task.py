from db.database import Base
from sqlalchemy.orm import relationship
from enum import Enum
from sqlalchemy import Column, String, Integer, Text, DateTime, Enum as EnumType, ForeignKey

class TaskStatus(Enum):
    TODO = "TODO",
    IN_PROGRESS = "IN_PROGRESS",
    DONE = "DONE"
    
class TaskPriority(Enum):
    LOW = "LOW",
    MEDIUM = "MEDIUM",
    HIGH = "HIGH"

class ResearchTask(Base):
    __tablename__ = "research_task"
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("research_projects.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(EnumType(TaskStatus, name="task_status_enum"), nullable=False)
    priority = Column(EnumType(TaskPriority, name="task_priority_enum"), nullable=False)
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False)

    project = relationship("research_project", back_populates="tasks")
    assignee = relationship("user", back_populates="tasks_assigned")