from sqlalchemy.orm import Session

from models.research_member import ResearchMembers, ResearchMemberRoles
from models.user import UserModel
from core.app_exceptions import AppException


def add_member(project_id, user_id, db: Session):
    """Thêm người dùng vào đề tài nếu chưa là thành viên."""
    target_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if target_user is None:
        raise AppException(status_code=404, message="Người dùng không tồn tại")

    existing = db.query(ResearchMembers).filter(
        ResearchMembers.project_id == project_id,
        ResearchMembers.user_id == user_id,
    ).first()
    if existing is not None:
        raise AppException(status_code=400, message="Người dùng đã là thành viên của đề tài nghiên cứu")

    try:
        new_member = ResearchMembers(project_id=project_id, user_id=user_id, role=ResearchMemberRoles.MEMBER)
        db.add(new_member)
        db.commit()
        db.refresh(new_member)
        return new_member
    except Exception:
        db.rollback()
        raise AppException(status_code=400, message="Không thể thêm thành viên")


def list_members(project_id, db: Session):
    """Lấy danh sách thành viên kèm thông tin người dùng."""
    rows = db.query(ResearchMembers, UserModel).join(UserModel, UserModel.id == ResearchMembers.user_id).filter(
        ResearchMembers.project_id == project_id
    ).all()

    result = []
    for member, user in rows:
        result.append({
            "user_id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "role": member.role,
            "joined_at": member.joined_at,
        })
    return result


def remove_member(project_id, user_id, db: Session):
    """Xóa thành viên nhưng giữ lại Owner cuối cùng."""
    member = db.query(ResearchMembers).filter(
        ResearchMembers.project_id == project_id,
        ResearchMembers.user_id == user_id,
    ).first()
    if member is None:
        raise AppException(status_code=404, message="Thành viên không tồn tại trong đề tài nghiên cứu")

    if member.role == ResearchMemberRoles.OWNER:
        owner_count = db.query(ResearchMembers).filter(
            ResearchMembers.project_id == project_id,
            ResearchMembers.role == ResearchMemberRoles.OWNER,
        ).count()
        if owner_count <= 1:
            raise AppException(status_code=400, message="Không thể xóa Owner cuối cùng của đề tài nghiên cứu")

    try:
        db.delete(member)
        db.commit()
    except Exception:
        db.rollback()
        raise AppException(status_code=400, message="Không thể xóa thành viên")
