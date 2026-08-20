from db.database import Base
from sqlalchemy import Text, String, Integer, Column, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class ResearchProject(Base):
    __tablename__ = "research_projects"
    
    id = Column(Integer, primary_key= True)
    name = Column(String(50), nullable= False)
    description = Column(Text, nullable= True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable= False)
    created_at = Column(DateTime, nullable=False)
    
    owner = relationship("user", back_populates="project_owned")
    members = relationship("research_member", back_populates="project")
    tasks = relationship("research_task", back_populates="project")