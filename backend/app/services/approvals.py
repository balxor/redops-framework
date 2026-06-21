from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.approval import Approval
from app.schemas.approval import ApprovalCreate, ApprovalDecision, ApprovalRead
from app.schemas.common import new_id, utc_now


def list_approvals(db: Session, project_id: str) -> list[ApprovalRead]:
    statement = select(Approval).where(Approval.project_id == project_id).order_by(Approval.created_at.desc())
    return [ApprovalRead.model_validate(approval) for approval in db.scalars(statement).all()]


def create_approval(db: Session, project_id: str, requested_by: str, payload: ApprovalCreate) -> ApprovalRead:
    now = utc_now()
    approval = Approval(
        approval_id=new_id("approval"),
        project_id=project_id,
        requested_by=requested_by,
        status="pending",
        requested_at=now,
        created_at=now,
        updated_at=now,
        **payload.model_dump(mode="json"),
    )
    db.add(approval)
    db.commit()
    db.refresh(approval)
    return ApprovalRead.model_validate(approval)


def decide_approval(
    db: Session,
    project_id: str,
    approval_id: str,
    decided_by: str,
    decision: ApprovalDecision,
    status_value: str,
) -> ApprovalRead | None:
    approval = db.get(Approval, approval_id)
    if approval is None or approval.project_id != project_id:
        return None
    if approval.status not in {"pending", "approved"}:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Only pending or approved approvals can receive this decision",
        )
    now = utc_now()
    approval.status = status_value
    approval.decided_by = decided_by
    approval.decision_note = decision.decision_note
    approval.decided_at = now
    approval.updated_at = now
    db.commit()
    db.refresh(approval)
    return ApprovalRead.model_validate(approval)


def has_active_approval(db: Session, project_id: str, entity_type: str, entity_id: str) -> bool:
    now = utc_now()
    statement = select(Approval).where(
        Approval.project_id == project_id,
        Approval.entity_type == entity_type,
        Approval.entity_id == entity_id,
        Approval.status == "approved",
    )
    approvals = db.scalars(statement).all()
    return any(approval.expires_at is None or approval.expires_at > now for approval in approvals)
