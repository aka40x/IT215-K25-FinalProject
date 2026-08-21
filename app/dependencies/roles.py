from fastapi import Depends

from core.exceptions import forbidden
from dependencies.auth import get_current_user
from models.user import UserModel, UserRoles


def require_admin(current_user: UserModel = Depends(get_current_user)):
    """Chỉ cho phép user có role Admin tiếp tục xử lý."""
    if current_user.role != UserRoles.ADMIN:
        raise forbidden("Chỉ Admin mới có quyền thực hiện thao tác này")
    return current_user