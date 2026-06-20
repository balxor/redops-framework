from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.rbac import get_current_user
from app.schemas.asset import AssetCreate, AssetRead, AssetUpdate
from app.schemas.user import CurrentUser
from app.services.memberships import PROJECT_WRITE_ROLES, ensure_project_access
from app.services.safety import validate_asset_create, validate_asset_update
from app.services.store import store

router = APIRouter()


@router.get("", response_model=list[AssetRead])
def list_assets(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> list[AssetRead]:
    ensure_project_access(db, current_user, project_id)
    return store.list_assets(db, project_id)


@router.post("", response_model=AssetRead, status_code=status.HTTP_201_CREATED)
def create_asset(
    project_id: str,
    payload: AssetCreate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> AssetRead:
    ensure_project_access(db, current_user, project_id, PROJECT_WRITE_ROLES | {"operator"})
    validate_asset_create(db, project_id, payload)
    return store.create_asset(db, project_id, payload)


@router.get("/{asset_id}", response_model=AssetRead)
def get_asset(
    project_id: str,
    asset_id: str,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> AssetRead:
    ensure_project_access(db, current_user, project_id)
    asset = store.get_asset(db, project_id, asset_id)
    if asset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")
    return asset


@router.patch("/{asset_id}", response_model=AssetRead)
def update_asset(
    project_id: str,
    asset_id: str,
    payload: AssetUpdate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> AssetRead:
    ensure_project_access(db, current_user, project_id, PROJECT_WRITE_ROLES | {"operator"})
    validate_asset_update(db, project_id, payload)
    asset = store.update_asset(db, project_id, asset_id, payload)
    if asset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")
    return asset


@router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_asset(
    project_id: str,
    asset_id: str,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> None:
    ensure_project_access(db, current_user, project_id, PROJECT_WRITE_ROLES)
    deleted = store.delete_asset(db, project_id, asset_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")
