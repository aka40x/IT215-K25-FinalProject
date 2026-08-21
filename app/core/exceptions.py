from fastapi import HTTPException, status


def bad_request(detail: str):
    """Tạo lỗi HTTP 400 cho dữ liệu hoặc thao tác không hợp lệ."""
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


def unauthorized(detail: str = "Unauthorized"):
    """Tạo lỗi HTTP 401 khi chưa xác thực hoặc token không hợp lệ."""
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


def forbidden(detail: str = "Forbidden"):
    """Tạo lỗi HTTP 403 khi user không đủ quyền."""
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


def not_found(detail: str = "Resource not found"):
    """Tạo lỗi HTTP 404 khi không tìm thấy tài nguyên."""
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)