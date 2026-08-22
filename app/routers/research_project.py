from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.orm import Session
from typing import Optional

from db.database import get_db
from dependencies.auth import get_current_user
from dependencies.permission_dependency import require_project_member, require_project_owner
from schemas.research_project import ResearchMemberCreate, ResearchProjectUpdate, ResearchProjectResponse
from schemas.research_member import MemberAdd, MemberOut
from services.research_project_service import (
    create_project, list_my_projects, get_project_detail, update_project, delete_project,
)
from services.research_member_service import add_member, list_members, remove_member
from core.responses import success_response

router = APIRouter(prefix="/research-projects", tags=["Research Projects"])


@router.post("", summary="Tạo đề tài nghiên cứu")
def create(request: Request, payload: ResearchMemberCreate, db: Session = Depends(get_db),
           current_user=Depends(get_current_user)):
    """Endpoint tạo đề tài nghiên cứu."""
    project = create_project(payload, current_user, db)
    data = ResearchProjectResponse.model_validate(project).model_dump(mode="json")
    return success_response(request, data=data, message="Tạo đề tài nghiên cứu thành công", status_code=201)


@router.get("", summary="Danh sách đề tài nghiên cứu của tôi")
def list_mine(request: Request, search: Optional[str] = Query(default=None), db: Session = Depends(get_db),
              current_user=Depends(get_current_user)):
    """Endpoint lấy danh sách đề tài của người dùng hiện tại."""
    projects = list_my_projects(current_user, db, search=search)
    data = [ResearchProjectResponse.model_validate(p).model_dump(mode="json") for p in projects]
    return success_response(request, data=data, message="Lấy danh sách đề tài nghiên cứu thành công")


@router.get("/{project_id}", summary="Chi tiết đề tài nghiên cứu")
def detail(request: Request, project_id: int, db: Session = Depends(get_db),
           current_user=Depends(require_project_member)):
    """Endpoint xem chi tiết một đề tài."""
    project = get_project_detail(project_id, db)
    data = ResearchProjectResponse.model_validate(project).model_dump(mode="json")
    return success_response(request, data=data, message="Lấy chi tiết đề tài nghiên cứu thành công")


@router.patch("/{project_id}", summary="Cập nhật đề tài nghiên cứu")
def update(request: Request, project_id: int, payload: ResearchProjectUpdate, db: Session = Depends(get_db),
           current_user=Depends(require_project_owner)):
    """Endpoint cập nhật đề tài bởi Owner."""
    project = update_project(project_id, payload, db)
    data = ResearchProjectResponse.model_validate(project).model_dump(mode="json")
    return success_response(request, data=data, message="Cập nhật đề tài nghiên cứu thành công")


@router.delete("/{project_id}", summary="Xóa đề tài nghiên cứu")
def delete(request: Request, project_id: int, db: Session = Depends(get_db),
           current_user=Depends(require_project_owner)):
    """Endpoint xóa đề tài bởi Owner."""
    delete_project(project_id, db)
    return success_response(request, data=None, message="Xóa đề tài nghiên cứu thành công")


@router.post("/{project_id}/members", summary="Thêm thành viên")
def add(request: Request, project_id: int, payload: MemberAdd, db: Session = Depends(get_db),
        current_user=Depends(require_project_owner)):
    """Endpoint thêm thành viên vào đề tài."""
    add_member(project_id, payload.user_id, db)
    return success_response(request, data=None, message="Thêm thành viên thành công", status_code=201)


@router.get("/{project_id}/members", summary="Danh sách thành viên")
def get_members(request: Request, project_id: int, db: Session = Depends(get_db),
                 current_user=Depends(require_project_member)):
    """Endpoint lấy danh sách thành viên của đề tài."""
    members = list_members(project_id, db)
    data = [MemberOut.model_validate(m).model_dump(mode="json") for m in members]
    return success_response(request, data=data, message="Lấy danh sách thành viên thành công")


@router.delete("/{project_id}/members/{user_id}", summary="Xóa thành viên")
def remove(request: Request, project_id: int, user_id: int, db: Session = Depends(get_db),
           current_user=Depends(require_project_owner)):
    """Endpoint xóa thành viên khỏi đề tài."""
    remove_member(project_id, user_id, db)
    return success_response(request, data=None, message="Xóa thành viên thành công")
