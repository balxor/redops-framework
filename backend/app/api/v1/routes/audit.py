from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.rbac import get_current_user
from app.schemas.audit import AuditLogRead
from app.schemas.user import CurrentUser
from app.services.audit import list_audit_logs
from app.services.memberships import ensure_project_access

router = APIRouter()


@router.get("", response_model=list[AuditLogRead])
def get_audit_logs(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> list[AuditLogRead]:
    ensure_project_access(db, current_user, project_id)
    return list_audit_logs(db, project_id)
