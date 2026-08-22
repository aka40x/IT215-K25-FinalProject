from fastapi import Depends
from sqlalchemy.orm import Session

from db.database import get_db
from dependencies.auth import get_current_user
from models.user import UserModel
from models.research_member import ResearchMembers, ResearchMemberRoles
from models.research_task import ResearchTask
from core.app_exceptions import AppException


def require_project_member(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Chỉ cho phép thành viên của đề tài tiếp tục xử lý."""
    member = db.query(ResearchMembers).filter(
        ResearchMembers.project_id == project_id,
        ResearchMembers.user_id == current_user.id,
    ).first()
    if member is None:
        raise AppException(status_code=403, message="Bạn không phải thành viên của đề tài nghiên cứu này")
    return current_user


def require_project_owner(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Chỉ cho phép Owner của đề tài tiếp tục xử lý."""
    member = db.query(ResearchMembers).filter(
        ResearchMembers.project_id == project_id,
        ResearchMembers.user_id == current_user.id,
    ).first()
    if member is None or member.role != ResearchMemberRoles.OWNER:
        raise AppException(status_code=403, message="Chỉ Owner mới có quyền thực hiện thao tác này")
    return current_user


def require_task_permission(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Kiểm tra người dùng có quyền thao tác trên nhiệm vụ."""
    task = db.query(ResearchTask).filter(ResearchTask.id == task_id).first()
    if task is None:
        raise AppException(status_code=404, message="Nhiệm vụ nghiên cứu không tồn tại")

    member = db.query(ResearchMembers).filter(
        ResearchMembers.project_id == task.project_id,
        ResearchMembers.user_id == current_user.id,
    ).first()
    if member is None:
        raise AppException(status_code=403, message="Bạn không có quyền thao tác với nhiệm vụ nghiên cứu này")
    return current_user
