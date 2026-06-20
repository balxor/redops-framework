from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.asset import AssetCreate, AssetRead, AssetUpdate
from app.services.store import store

router = APIRouter()


@router.get("", response_model=list[AssetRead])
def list_assets(project_id: str, db: Session = Depends(get_db)) -> list[AssetRead]:
    ensure_project(db, project_id)
    return store.list_assets(db, project_id)


@router.post("", response_model=AssetRead, status_code=status.HTTP_201_CREATED)
def create_asset(project_id: str, payload: AssetCreate, db: Session = Depends(get_db)) -> AssetRead:
    ensure_project(db, project_id)
    return store.create_asset(db, project_id, payload)


@router.get("/{asset_id}", response_model=AssetRead)
def get_asset(project_id: str, asset_id: str, db: Session = Depends(get_db)) -> AssetRead:
    ensure_project(db, project_id)
    asset = store.get_asset(db, project_id, asset_id)
    if asset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")
    return asset


@router.patch("/{asset_id}", response_model=AssetRead)
def update_asset(project_id: str, asset_id: str, payload: AssetUpdate, db: Session = Depends(get_db)) -> AssetRead:
    ensure_project(db, project_id)
    asset = store.update_asset(db, project_id, asset_id, payload)
    if asset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")
    return asset


@router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_asset(project_id: str, asset_id: str, db: Session = Depends(get_db)) -> None:
    ensure_project(db, project_id)
    deleted = store.delete_asset(db, project_id, asset_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")


def ensure_project(db: Session, project_id: str) -> None:
    if store.get_project(db, project_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
