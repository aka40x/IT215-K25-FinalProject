from db.database import Base
from enum import Enum
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Enum as EnumType, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship

class ResearchMemberRoles(Enum):
    """Các vai trò của thành viên trong đề tài."""
    OWNER = "OWNER"
    MEMBER = "MEMBER"

class ResearchMembers(Base):
    """Model trung gian liên kết user với đề tài nghiên cứu."""
    __tablename__ = "research_members"
    __table_args__ = (UniqueConstraint("project_id", "user_id", name="uq_project_user"),)
    
    project_id = Column(Integer, ForeignKey("research_projects.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    role = Column(EnumType(ResearchMemberRoles, name="member_role_enum"), nullable=False)
    joined_at = Column(DateTime, default=datetime.utcnow, nullable=False)    
    
    project = relationship("ResearchProject", back_populates="members")
    user = relationship("UserModel", back_populates="memberships")