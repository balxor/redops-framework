from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.rbac import get_current_user
from app.schemas.report import ReportCreate, ReportRead, ReportUpdate
from app.schemas.user import CurrentUser
from app.services.memberships import PROJECT_WRITE_ROLES, ensure_project_access
from app.services.store import store

router = APIRouter()


@router.get("", response_model=list[ReportRead])
def list_reports(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> list[ReportRead]:
    ensure_project_access(db, current_user, project_id)
    return store.list_reports(db, project_id)


@router.post("", response_model=ReportRead, status_code=status.HTTP_201_CREATED)
def create_report(
    project_id: str,
    payload: ReportCreate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> ReportRead:
    ensure_project_access(db, current_user, project_id, PROJECT_WRITE_ROLES | {"operator"})
    return store.create_report(db, project_id, payload)


@router.get("/{report_id}", response_model=ReportRead)
def get_report(
    project_id: str,
    report_id: str,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> ReportRead:
    ensure_project_access(db, current_user, project_id)
    report = store.get_report(db, project_id, report_id)
    if report is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    return report


@router.patch("/{report_id}", response_model=ReportRead)
def update_report(
    project_id: str,
    report_id: str,
    payload: ReportUpdate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> ReportRead:
    ensure_project_access(db, current_user, project_id, PROJECT_WRITE_ROLES | {"reviewer"})
    report = store.update_report(db, project_id, report_id, payload)
    if report is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    return report

