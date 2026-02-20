from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.common.dto import UserOut, UserPublic, UserUpdate
from app.database.db_connection import get_db
from app.users.users_service import get_current_user, get_user_or_404
from app.users import users_repository

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/search/", response_model=List[UserPublic])
def search_users(
    q: str = Query(..., min_length=1),
    limit: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db),
):
    return users_repository.search(db, q=q, limit=limit)


@router.get("/{user_id}", response_model=UserPublic)
def get_profile(user_id: int, db: Session = Depends(get_db)):
    return get_user_or_404(db, user_id)


@router.patch("/me", response_model=UserOut)
def update_me(payload: UserUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return users_repository.update_profile(db, current_user, bio=payload.bio, avatar_url=payload.avatar_url)
