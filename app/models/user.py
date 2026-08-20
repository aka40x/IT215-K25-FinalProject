from db.database import Base
from enum import Enum
from sqlalchemy import Column, String, Integer, Boolean, Enum as EnumType, DateTime
from sqlalchemy.orm import relationship

class UserRoles(Enum):
    USER = "USER",
    ADMIN = "ADMIN"

class UserModel(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key = True)
    email = Column(String(50), unique= True, nullable= False)
    password_hash = Column(String(255), nullable= False)
    full_name = Column(String(50), nullable= False)
    role = Column(EnumType(UserRoles), name="user_role_enum", default= UserRoles.USER)
    is_active = Column(Boolean, default= True, nullable= False)
    created_at = Column(DateTime, nullable= False)
    
    project_owned = relationship("ResearchProject", back_populates="owner")
    memberships = relationship("ResearchMember", back_populates="user")
    tasks_assigned = relationship("ResearchTask", back_populates="assignee")