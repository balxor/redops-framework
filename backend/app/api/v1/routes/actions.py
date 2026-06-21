from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.rbac import get_current_user
from app.schemas.action import ActionCreate, ActionRead, ActionUpdate
from app.schemas.user import CurrentUser
from app.services.audit import record_audit_event
from app.services.memberships import PROJECT_WRITE_ROLES, ensure_project_access
from app.services.safety import validate_action_create, validate_action_update
from app.services.store import store

router = APIRouter()


@router.get("", response_model=list[ActionRead])
def list_actions(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> list[ActionRead]:
    ensure_project_access(db, current_user, project_id)
    return store.list_actions(db, project_id)


@router.post("", response_model=ActionRead, status_code=status.HTTP_201_CREATED)
def create_action(
    project_id: str,
    payload: ActionCreate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> ActionRead:
    ensure_project_access(db, current_user, project_id, PROJECT_WRITE_ROLES | {"operator"})
    validate_action_create(db, project_id, payload)
    action = store.create_action(db, project_id, current_user.user_id, payload)
    record_audit_event(
        db,
        project_id=project_id,
        actor_user_id=current_user.user_id,
        action="action.created",
        resource_type="action",
        resource_id=action.action_id,
        summary=f"Action logged: {action.action_summary}",
    )
    return action


@router.get("/{action_id}", response_model=ActionRead)
def get_action(
    project_id: str,
    action_id: str,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> ActionRead:
    ensure_project_access(db, current_user, project_id)
    action = store.get_action(db, project_id, action_id)
    if action is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Action not found")
    return action


@router.patch("/{action_id}", response_model=ActionRead)
def update_action(
    project_id: str,
    action_id: str,
    payload: ActionUpdate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> ActionRead:
    ensure_project_access(db, current_user, project_id, PROJECT_WRITE_ROLES | {"operator"})
    validate_action_update(db, project_id, payload)
    action = store.update_action(db, project_id, action_id, payload)
    if action is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Action not found")
    record_audit_event(
        db,
        project_id=project_id,
        actor_user_id=current_user.user_id,
        action="action.updated",
        resource_type="action",
        resource_id=action_id,
        summary=f"Action updated: {action.action_summary}",
    )
    return action
