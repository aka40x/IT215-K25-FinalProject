from sqlalchemy.orm import Session

from models.research_project import ResearchProject
from models.research_member import ResearchMemberRoles, ResearchMembers
from schemas.research_project import ResearchProjectCreate, ResearchProjectUpdate, ResearchProjectResponse
from core.app_exceptions import AppException

def create_project(payload: ResearchProjectCreate, current_user, db: Session):
    """ Tạo đề tài và tự thêm người tạo làm Owner """
    try:
        new_project = ResearchProject(
            name = payload.name,
            description = payload.description,
            owner_id = current_user.id,
        )
        db.add(new_project)
        db.flush()
        
        owner_member = ResearchMembers(
            project_id = new_project.id,
            user_id = current_user.id,
            role = ResearchMemberRoles.OWNER,
        )
        db.add(owner_member)
        db.commit()
        db.refresh(new_project)
        return new_project
    except Exception:
        db.rollback()
        raise AppException(status_code=400, message="Không thể tạo đề tài nghiên cứu")

def list_my_projects(current_user, db: Session, search = None):
    """Lấy các đề tài mà người dùng hiện tại tham gia"""
    query = db.query(ResearchProject).join(ResearchMembers, ResearchMembers.project_id == ResearchProject.id).filter(ResearchMembers.user_id == current_user.id)
    
    if search is not None and search != "":
        like_pattern = "%" + search + "%"
        query = query.filter(ResearchProject.name.like(like_pattern))
        
    return query.all()

def get_project_detail(project_id, db: Session):
    """Tìm đề tài theo ID hoặc báo không tồn tại"""
    project = db.query(ResearchProject).filter(ResearchProject.id == project_id).first()
    if project is None:
        raise AppException(status_code=404, message="Đề tài nghiên cứu không tồn tại")
    return project

def update_project(project_id, payload: ResearchProjectUpdate, db: Session):
    """Cập nhật các trường được gửi lên của đề tài"""
    project = get_project_detail(project_id, db)
    update_data = payload.model_dump(exclude_unset=True)
    try:
        for key, value in update_data.items():
            setattr(project, key, value)
        db.commit()
        db.refresh(project)
        return project
    except Exception:
        db.rollback()
        raise AppException(status_code=400, message="Không thể cập nhật đề tài nghiên cứu")
    
def delete_project(project_id, db: Session):
    """Xóa đề tài nghiên cứu theo ID"""
    project = get_project_detail(project_id, db)
    try:
        db.delete(project)
        db.commit()
    except Exception:
        db.rollback()
        raise AppException(status_code=400, message="Không thể xóa đề tài nghiên cứu")
