from db.database import Base
from sqlalchemy.orm import relationship
from enum import Enum
from sqlalchemy import Column, String, Integer, Text, DateTime, Enum as EnumType, ForeignKey

class TaskStatus(Enum):
    """Các trạng thái xử lý của nhiệm vụ."""
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    
class TaskPriority(Enum):
    """Các mức độ ưu tiên của nhiệm vụ."""
    LOW = "LOW",
    MEDIUM = "MEDIUM",
    HIGH = "HIGH"

class ResearchTask(Base):
    """Model lưu nhiệm vụ thuộc một đề tài nghiên cứu."""
    __tablename__ = "research_tasks"
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("research_projects.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(EnumType(TaskStatus, name="task_status_enum"), nullable=False)
    priority = Column(EnumType(TaskPriority, name="task_priority_enum"), nullable=False)
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False)

    project = relationship("ResearchProject", back_populates="tasks")
    assignee = relationship("UserModel", back_populates="tasks_assigned")