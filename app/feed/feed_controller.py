from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.common.dto import FeedOut
from app.common.utils import clamp_pagination
from app.database.db_connection import get_db
from app.feed.feed_service import get_feed_posts
from app.posts.posts_controller import _to_post_out
from app.users.users_service import get_current_user

router = APIRouter(prefix="/feed", tags=["feed"])


@router.get("/", response_model=FeedOut)
def feed(limit: int = Query(20, ge=1, le=50), offset: int = Query(0, ge=0),
         db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    limit, offset = clamp_pagination(limit, offset)
    posts, total = get_feed_posts(db, user_id=current_user.id, limit=limit, offset=offset)
    return FeedOut(items=[_to_post_out(db, p) for p in posts], limit=limit, offset=offset, total=total)
