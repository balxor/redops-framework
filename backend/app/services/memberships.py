from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.membership import ProjectMember
from app.models.project import Project
from app.models.user import User
from app.schemas.common import new_id, utc_now
from app.schemas.membership import ProjectMemberCreate, ProjectMemberRead, ProjectMemberUpdate
from app.schemas.user import CurrentUser

PROJECT_READ_ROLES = {"lead_operator", "operator", "reviewer", "client_viewer"}
PROJECT_WRITE_ROLES = {"lead_operator"}


def list_project_members(db: Session, project_id: str) -> list[ProjectMemberRead]:
    statement = select(ProjectMember).where(ProjectMember.project_id == project_id).order_by(ProjectMember.created_at)
    return [member_to_read(member) for member in db.scalars(statement).all()]


def create_project_member(db: Session, project_id: str, payload: ProjectMemberCreate) -> ProjectMemberRead:
    if db.get(Project, project_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    if db.get(User, payload.user_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    now = utc_now()
    member = ProjectMember(
        project_member_id=new_id("project_member"),
        project_id=project_id,
        user_id=payload.user_id,
        project_role=payload.project_role,
        created_at=now,
        updated_at=now,
    )
    db.add(member)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User is already a project member") from exc
    db.refresh(member)
    return member_to_read(member)


def update_project_member(
    db: Session,
    project_id: str,
    project_member_id: str,
    payload: ProjectMemberUpdate,
) -> ProjectMemberRead | None:
    member = db.get(ProjectMember, project_member_id)
    if member is None or member.project_id != project_id:
        return None
    member.project_role = payload.project_role
    member.updated_at = utc_now()
    db.commit()
    db.refresh(member)
    return member_to_read(member)


def delete_project_member(db: Session, project_id: str, project_member_id: str) -> bool:
    member = db.get(ProjectMember, project_member_id)
    if member is None or member.project_id != project_id:
        return False
    db.delete(member)
    db.commit()
    return True


def add_project_owner(db: Session, project_id: str, user_id: str) -> ProjectMemberRead:
    existing = db.scalar(
        select(ProjectMember).where(ProjectMember.project_id == project_id, ProjectMember.user_id == user_id)
    )
    if existing:
        return member_to_read(existing)
    return create_project_member(
        db,
        project_id,
        ProjectMemberCreate(user_id=user_id, project_role="lead_operator"),
    )


def accessible_project_ids(db: Session, current_user: CurrentUser) -> list[str] | None:
    if "admin" in current_user.roles:
        return None
    statement = select(ProjectMember.project_id).where(ProjectMember.user_id == current_user.user_id)
    return list(db.scalars(statement).all())


def ensure_project_access(
    db: Session,
    current_user: CurrentUser,
    project_id: str,
    allowed_project_roles: set[str] | None = None,
) -> None:
    if "admin" in current_user.roles:
        return

    project = db.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    member = db.scalar(
        select(ProjectMember).where(ProjectMember.project_id == project_id, ProjectMember.user_id == current_user.user_id)
    )
    if member is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Project membership required")

    allowed = allowed_project_roles or PROJECT_READ_ROLES
    if member.project_role not in allowed:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient project role")


def member_to_read(member: ProjectMember) -> ProjectMemberRead:
    return ProjectMemberRead(
        project_member_id=member.project_member_id,
        project_id=member.project_id,
        user_id=member.user_id,
        project_role=member.project_role,
        created_at=member.created_at,
        updated_at=member.updated_at,
    )

