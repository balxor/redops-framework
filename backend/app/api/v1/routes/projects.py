from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.rbac import get_current_user
from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate
from app.schemas.user import CurrentUser
from app.services.audit import record_audit_event
from app.services.memberships import PROJECT_WRITE_ROLES, accessible_project_ids, add_project_owner, ensure_project_access
from app.services.store import store

router = APIRouter()


@router.get("", response_model=list[ProjectRead])
def list_projects(
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> list[ProjectRead]:
    return store.list_projects(db, accessible_project_ids(db, current_user))


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(
    payload: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> ProjectRead:
    project = store.create_project(db, payload)
    add_project_owner(db, project.project_id, current_user.user_id)
    record_audit_event(
        db,
        project_id=project.project_id,
        actor_user_id=current_user.user_id,
        action="project.created",
        resource_type="project",
        resource_id=project.project_id,
        summary=f"Project created: {project.name}",
    )
    return project


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> ProjectRead:
    ensure_project_access(db, current_user, project_id)
    project = store.get_project(db, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


@router.patch("/{project_id}", response_model=ProjectRead)
def update_project(
    project_id: str,
    payload: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> ProjectRead:
    ensure_project_access(db, current_user, project_id, PROJECT_WRITE_ROLES)
    project = store.update_project(db, project_id, payload)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    record_audit_event(
        db,
        project_id=project_id,
        actor_user_id=current_user.user_id,
        action="project.updated",
        resource_type="project",
        resource_id=project_id,
        summary=f"Project updated: {project.name}",
    )
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> None:
    ensure_project_access(db, current_user, project_id, PROJECT_WRITE_ROLES)
    deleted = store.delete_project(db, project_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    record_audit_event(
        db,
        project_id=project_id,
        actor_user_id=current_user.user_id,
        action="project.deleted",
        resource_type="project",
        resource_id=project_id,
        summary="Project deleted",
    )
