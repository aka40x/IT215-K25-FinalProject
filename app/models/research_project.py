from db.database import Base
from sqlalchemy import Text, String, Integer, Column, DateTime, ForeignKey
from datetime import datetime 
from sqlalchemy.orm import relationship

class ResearchProject(Base):
    """Model lưu thông tin đề tài nghiên cứu."""
    __tablename__ = "research_projects"
    
    id = Column(Integer, primary_key= True)
    name = Column(String(50), nullable= False)
    description = Column(Text, nullable= True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable= False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)    
    
    owner = relationship("UserModel", back_populates="project_owned")
    members = relationship("ResearchMembers", back_populates="project")
    tasks = relationship("ResearchTask", back_populates="project")