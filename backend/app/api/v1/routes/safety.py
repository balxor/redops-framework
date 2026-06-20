from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.rbac import get_current_user
from app.schemas.safety import SafetySummary
from app.schemas.user import CurrentUser
from app.services.memberships import ensure_project_access
from app.services.safety import get_safety_summary

router = APIRouter()


@router.get("/summary", response_model=SafetySummary)
def safety_summary(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> SafetySummary:
    ensure_project_access(db, current_user, project_id)
    return get_safety_summary(db, project_id)

