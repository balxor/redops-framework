from fastapi import APIRouter, HTTPException, status

from app.schemas.campaign import CampaignCreate, CampaignRead, CampaignUpdate
from app.services.store import store

router = APIRouter()


@router.get("", response_model=list[CampaignRead])
def list_campaigns(project_id: str) -> list[CampaignRead]:
    ensure_project(project_id)
    return store.list_campaigns(project_id)


@router.post("", response_model=CampaignRead, status_code=status.HTTP_201_CREATED)
def create_campaign(project_id: str, payload: CampaignCreate) -> CampaignRead:
    ensure_project(project_id)
    return store.create_campaign(project_id, payload)


@router.get("/{campaign_id}", response_model=CampaignRead)
def get_campaign(project_id: str, campaign_id: str) -> CampaignRead:
    ensure_project(project_id)
    campaign = store.get_campaign(project_id, campaign_id)
    if campaign is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found")
    return campaign


@router.patch("/{campaign_id}", response_model=CampaignRead)
def update_campaign(project_id: str, campaign_id: str, payload: CampaignUpdate) -> CampaignRead:
    ensure_project(project_id)
    campaign = store.update_campaign(project_id, campaign_id, payload)
    if campaign is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found")
    return campaign


def ensure_project(project_id: str) -> None:
    if store.get_project(project_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

