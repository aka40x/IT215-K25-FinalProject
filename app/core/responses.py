from datetime import datetime
from fastapi import Request
from fastapi.responses import JSONResponse


def success_response(request: Request, data=None, message="Thành công", status_code=200):
    """Tạo response thành công theo format thống nhất của API."""
    content = {
        "statusCode": status_code,
        "message": message,
        "error": None,
        "data": data,
        "path": str(request.url.path),
        "timestamp": datetime.utcnow().isoformat(),
    }
    return JSONResponse(status_code=status_code, content=content)


def error_response(request: Request, message="Có lỗi xảy ra", status_code=400, error="Bad Request"):
    """Tạo response lỗi theo format thống nhất của API."""
    content = {
        "statusCode": status_code,
        "message": message,
        "error": error,
        "data": None,
        "path": str(request.url.path),
        "timestamp": datetime.utcnow().isoformat(),
    }
    return JSONResponse(status_code=status_code, content=content)
