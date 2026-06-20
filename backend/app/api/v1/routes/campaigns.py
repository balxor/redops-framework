from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.rbac import get_current_user
from app.schemas.campaign import CampaignCreate, CampaignRead, CampaignUpdate
from app.schemas.user import CurrentUser
from app.services.memberships import PROJECT_WRITE_ROLES, ensure_project_access
from app.services.store import store

router = APIRouter()


@router.get("", response_model=list[CampaignRead])
def list_campaigns(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> list[CampaignRead]:
    ensure_project_access(db, current_user, project_id)
    return store.list_campaigns(db, project_id)


@router.post("", response_model=CampaignRead, status_code=status.HTTP_201_CREATED)
def create_campaign(
    project_id: str,
    payload: CampaignCreate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> CampaignRead:
    ensure_project_access(db, current_user, project_id, PROJECT_WRITE_ROLES)
    return store.create_campaign(db, project_id, payload)


@router.get("/{campaign_id}", response_model=CampaignRead)
def get_campaign(
    project_id: str,
    campaign_id: str,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> CampaignRead:
    ensure_project_access(db, current_user, project_id)
    campaign = store.get_campaign(db, project_id, campaign_id)
    if campaign is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found")
    return campaign


@router.patch("/{campaign_id}", response_model=CampaignRead)
def update_campaign(
    project_id: str,
    campaign_id: str,
    payload: CampaignUpdate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> CampaignRead:
    ensure_project_access(db, current_user, project_id, PROJECT_WRITE_ROLES)
    campaign = store.update_campaign(db, project_id, campaign_id, payload)
    if campaign is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found")
    return campaign

