from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.rbac import get_current_user
from app.schemas.scope import ScopeCreate, ScopeRead, ScopeUpdate
from app.schemas.user import CurrentUser
from app.services.memberships import PROJECT_WRITE_ROLES, ensure_project_access
from app.services.store import store

router = APIRouter()


@router.get("", response_model=list[ScopeRead])
def list_scopes(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> list[ScopeRead]:
    ensure_project_access(db, current_user, project_id)
    return store.list_scopes(db, project_id)


@router.post("", response_model=ScopeRead, status_code=status.HTTP_201_CREATED)
def create_scope(
    project_id: str,
    payload: ScopeCreate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> ScopeRead:
    ensure_project_access(db, current_user, project_id, PROJECT_WRITE_ROLES)
    return store.create_scope(db, project_id, payload)


@router.get("/{scope_id}", response_model=ScopeRead)
def get_scope(
    project_id: str,
    scope_id: str,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> ScopeRead:
    ensure_project_access(db, current_user, project_id)
    scope = store.get_scope(db, project_id, scope_id)
    if scope is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scope not found")
    return scope


@router.patch("/{scope_id}", response_model=ScopeRead)
def update_scope(
    project_id: str,
    scope_id: str,
    payload: ScopeUpdate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> ScopeRead:
    ensure_project_access(db, current_user, project_id, PROJECT_WRITE_ROLES)
    scope = store.update_scope(db, project_id, scope_id, payload)
    if scope is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scope not found")
    return scope

