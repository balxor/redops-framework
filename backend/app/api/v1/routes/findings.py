from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.rbac import get_current_user
from app.schemas.finding import FindingCreate, FindingRead, FindingUpdate
from app.schemas.user import CurrentUser
from app.services.audit import record_audit_event
from app.services.memberships import PROJECT_WRITE_ROLES, ensure_project_access
from app.services.store import store

router = APIRouter()


@router.get("", response_model=list[FindingRead])
def list_findings(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> list[FindingRead]:
    ensure_project_access(db, current_user, project_id)
    return store.list_findings(db, project_id)


@router.post("", response_model=FindingRead, status_code=status.HTTP_201_CREATED)
def create_finding(
    project_id: str,
    payload: FindingCreate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> FindingRead:
    ensure_project_access(db, current_user, project_id, PROJECT_WRITE_ROLES | {"operator"})
    finding = store.create_finding(db, project_id, current_user.user_id, payload)
    record_audit_event(
        db,
        project_id=project_id,
        actor_user_id=current_user.user_id,
        action="finding.created",
        resource_type="finding",
        resource_id=finding.finding_id,
        summary=f"Finding created: {finding.title}",
    )
    return finding


@router.get("/{finding_id}", response_model=FindingRead)
def get_finding(
    project_id: str,
    finding_id: str,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> FindingRead:
    ensure_project_access(db, current_user, project_id)
    finding = store.get_finding(db, project_id, finding_id)
    if finding is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Finding not found")
    return finding


@router.patch("/{finding_id}", response_model=FindingRead)
def update_finding(
    project_id: str,
    finding_id: str,
    payload: FindingUpdate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> FindingRead:
    ensure_project_access(db, current_user, project_id, PROJECT_WRITE_ROLES | {"operator", "reviewer"})
    finding = store.update_finding(db, project_id, finding_id, payload)
    if finding is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Finding not found")
    record_audit_event(
        db,
        project_id=project_id,
        actor_user_id=current_user.user_id,
        action="finding.updated",
        resource_type="finding",
        resource_id=finding_id,
        summary=f"Finding updated: {finding.title}",
    )
    return finding
