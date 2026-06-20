from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.services.auth import create_user, get_user_read, list_users, update_user

router = APIRouter()


@router.get("", response_model=list[UserRead])
def get_users(db: Session = Depends(get_db)) -> list[UserRead]:
    return list_users(db)


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def post_user(payload: UserCreate, db: Session = Depends(get_db)) -> UserRead:
    try:
        return create_user(db, payload)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User email already exists") from exc
    except ValueError as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: str, db: Session = Depends(get_db)) -> UserRead:
    user = get_user_read(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=UserRead)
def patch_user(user_id: str, payload: UserUpdate, db: Session = Depends(get_db)) -> UserRead:
    try:
        user = update_user(db, user_id, payload)
    except ValueError as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
