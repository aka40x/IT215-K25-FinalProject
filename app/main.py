from fastapi import FastAPI

from db.database import Base, engine
from models import (UserRoles, ResearchProject, ResearchMembers, ResearchTask)

from routers.health import router as health_router


Base.metadata.create_all(bind=engine)


app = FastAPI(title="Research Management API", description="API quản lý đề tài và nhiệm vụ nghiên cứu", version="1.0.0")


app.include_router(health_router)


@app.get("/")
def root():
    return {"message": "Research Management API", "version": "1.0.0", "docs": "/docs"}