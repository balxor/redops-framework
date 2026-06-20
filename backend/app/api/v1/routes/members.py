from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.rbac import get_current_user
from app.schemas.membership import ProjectMemberCreate, ProjectMemberRead, ProjectMemberUpdate
from app.schemas.user import CurrentUser
from app.services.memberships import (
    PROJECT_WRITE_ROLES,
    create_project_member,
    delete_project_member,
    ensure_project_access,
    list_project_members,
    update_project_member,
)

router = APIRouter()


@router.get("", response_model=list[ProjectMemberRead])
def get_members(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> list[ProjectMemberRead]:
    ensure_project_access(db, current_user, project_id)
    return list_project_members(db, project_id)


@router.post("", response_model=ProjectMemberRead, status_code=status.HTTP_201_CREATED)
def post_member(
    project_id: str,
    payload: ProjectMemberCreate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> ProjectMemberRead:
    ensure_project_access(db, current_user, project_id, PROJECT_WRITE_ROLES)
    return create_project_member(db, project_id, payload)


@router.patch("/{project_member_id}", response_model=ProjectMemberRead)
def patch_member(
    project_id: str,
    project_member_id: str,
    payload: ProjectMemberUpdate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> ProjectMemberRead:
    ensure_project_access(db, current_user, project_id, PROJECT_WRITE_ROLES)
    member = update_project_member(db, project_id, project_member_id, payload)
    if member is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project member not found")
    return member


@router.delete("/{project_member_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_member(
    project_id: str,
    project_member_id: str,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> None:
    ensure_project_access(db, current_user, project_id, PROJECT_WRITE_ROLES)
    deleted = delete_project_member(db, project_id, project_member_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project member not found")

