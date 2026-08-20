from db.database import Base
from enum import Enum
from sqlalchemy import Column, String, Integer, DateTime, Enum as EnumType, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship

class ResearchMemberRoles(Enum):
    OWNER = "OWNER",
    MEMBER = "MEMBER"

class ResearchMembers(Base):
    __tablename__ = "research_members"
    __table_args__ = (UniqueConstraint("project_id", "user_id", name="uq_project_user"),)
    
    project_id = Column(Integer, ForeignKey("research_projects.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    role = Column(EnumType(ResearchMemberRoles, name="member_role_enum"), nullable=False)
    joined_at = Column(DateTime, nullable= False)
    
    project = relationship("research_project", back_populates="members")
    user = relationship("user", back_populates="memberships")