from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.common.dto import UserPublic
from app.common.utils import clamp_pagination
from app.database.db_connection import get_db
from app.social import follow_service, follow_repository
from app.users.users_service import get_current_user

router = APIRouter(prefix="/social", tags=["social"])


@router.post("/follow/{user_id}")
def follow(user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    follow_service.follow_user(db, follower_id=current_user.id, following_id=user_id)
    return {"status": "following"}


@router.delete("/follow/{user_id}")
def unfollow(user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    follow_service.unfollow_user(db, follower_id=current_user.id, following_id=user_id)
    return {"status": "unfollowed"}


@router.get("/followers/{user_id}")
def followers(user_id: int, limit: int = Query(20, ge=1, le=50), offset: int = Query(0, ge=0),
              db: Session = Depends(get_db)):
    limit, offset = clamp_pagination(limit, offset)
    items, total = follow_repository.list_followers(db, user_id=user_id, limit=limit, offset=offset)
    return {"items": [UserPublic.model_validate(u) for u in items], "limit": limit, "offset": offset, "total": total}


@router.get("/following/{user_id}")
def following(user_id: int, limit: int = Query(20, ge=1, le=50), offset: int = Query(0, ge=0),
              db: Session = Depends(get_db)):
    limit, offset = clamp_pagination(limit, offset)
    items, total = follow_repository.list_following(db, user_id=user_id, limit=limit, offset=offset)
    return {"items": [UserPublic.model_validate(u) for u in items], "limit": limit, "offset": offset, "total": total}
