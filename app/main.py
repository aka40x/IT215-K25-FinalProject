from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError

from core.app_exceptions import AppException
from core.responses import error_response

from db.database import Base, engine
import models

from routers.auth import router as auth_router
from routers.health import router as health_router
from routers.users import router as users_router
from routers.research_project import router as research_router


Base.metadata.create_all(bind=engine)


app = FastAPI(title="Research Management API", description="API quản lý đề tài và nhiệm vụ nghiên cứu", version="1.0.0")

@app.exception_handler(AppException)
def handle_app_exception(request: Request, exc: AppException):
    """Chuyển lỗi nghiệp vụ thành response chuẩn của API."""
    return error_response(request, message=exc.message, status_code=exc.status_code, error=exc.error)


@app.exception_handler(RequestValidationError)
def handle_validation_exception(request: Request, exc: RequestValidationError):
    """Chuyển lỗi validation đầu vào thành response 422."""
    return error_response(
        request,
        message="Dữ liệu đầu vào không hợp lệ",
        status_code=422,
        error=str(exc.errors()),
    )

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(research_router)


@app.get("/")
def root():
    """Trả về thông tin cơ bản và đường dẫn tài liệu API."""
    return {"message": "Research Management API", "version": "1.0.0", "docs": "/docs"}