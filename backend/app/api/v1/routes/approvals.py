from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.rbac import get_current_user
from app.schemas.approval import ApprovalCreate, ApprovalDecision, ApprovalRead
from app.schemas.user import CurrentUser
from app.services.approvals import create_approval, decide_approval, list_approvals
from app.services.audit import record_audit_event
from app.services.memberships import PROJECT_WRITE_ROLES, ensure_project_access

router = APIRouter()


@router.get("", response_model=list[ApprovalRead])
def get_approvals(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> list[ApprovalRead]:
    ensure_project_access(db, current_user, project_id)
    return list_approvals(db, project_id)


@router.post("", response_model=ApprovalRead, status_code=status.HTTP_201_CREATED)
def post_approval(
    project_id: str,
    payload: ApprovalCreate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> ApprovalRead:
    ensure_project_access(db, current_user, project_id, PROJECT_WRITE_ROLES | {"operator"})
    approval = create_approval(db, project_id, current_user.user_id, payload)
    record_audit_event(
        db,
        project_id=project_id,
        actor_user_id=current_user.user_id,
        action="approval.requested",
        resource_type="approval",
        resource_id=approval.approval_id,
        summary=f"Approval requested for {approval.entity_type}: {approval.entity_id}",
    )
    return approval


@router.post("/{approval_id}/approve", response_model=ApprovalRead)
def approve(
    project_id: str,
    approval_id: str,
    payload: ApprovalDecision,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> ApprovalRead:
    ensure_project_access(db, current_user, project_id, PROJECT_WRITE_ROLES)
    approval = decide_approval(db, project_id, approval_id, current_user.user_id, payload, "approved")
    if approval is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Approval not found")
    record_audit_event(
        db,
        project_id=project_id,
        actor_user_id=current_user.user_id,
        action="approval.approved",
        resource_type="approval",
        resource_id=approval_id,
        summary=f"Approval granted for {approval.entity_type}: {approval.entity_id}",
    )
    return approval


@router.post("/{approval_id}/reject", response_model=ApprovalRead)
def reject(
    project_id: str,
    approval_id: str,
    payload: ApprovalDecision,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> ApprovalRead:
    ensure_project_access(db, current_user, project_id, PROJECT_WRITE_ROLES)
    approval = decide_approval(db, project_id, approval_id, current_user.user_id, payload, "rejected")
    if approval is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Approval not found")
    record_audit_event(
        db,
        project_id=project_id,
        actor_user_id=current_user.user_id,
        action="approval.rejected",
        resource_type="approval",
        resource_id=approval_id,
        summary=f"Approval rejected for {approval.entity_type}: {approval.entity_id}",
    )
    return approval


@router.post("/{approval_id}/revoke", response_model=ApprovalRead)
def revoke(
    project_id: str,
    approval_id: str,
    payload: ApprovalDecision,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> ApprovalRead:
    ensure_project_access(db, current_user, project_id, PROJECT_WRITE_ROLES)
    approval = decide_approval(db, project_id, approval_id, current_user.user_id, payload, "revoked")
    if approval is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Approval not found")
    record_audit_event(
        db,
        project_id=project_id,
        actor_user_id=current_user.user_id,
        action="approval.revoked",
        resource_type="approval",
        resource_id=approval_id,
        summary=f"Approval revoked for {approval.entity_type}: {approval.entity_id}",
    )
    return approval
