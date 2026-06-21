from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.audit import AuditLog
from app.schemas.audit import AuditLogRead
from app.schemas.common import new_id, utc_now


def list_audit_logs(db: Session, project_id: str) -> list[AuditLogRead]:
    statement = (
        select(AuditLog)
        .where(AuditLog.project_id == project_id)
        .order_by(AuditLog.created_at.desc())
    )
    return [AuditLogRead.model_validate(log) for log in db.scalars(statement).all()]


def record_audit_event(
    db: Session,
    *,
    project_id: str,
    actor_user_id: str,
    action: str,
    resource_type: str,
    summary: str,
    resource_id: str | None = None,
    detail: dict[str, str | int | float | bool | None] | None = None,
) -> AuditLogRead:
    log = AuditLog(
        audit_log_id=new_id("audit"),
        project_id=project_id,
        actor_user_id=actor_user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        summary=summary,
        detail=detail or {},
        created_at=utc_now(),
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return AuditLogRead.model_validate(log)
