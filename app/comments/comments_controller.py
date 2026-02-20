from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.common.dto import CommentCreate, CommentOut
from app.common.utils import clamp_pagination
from app.comments import comments_repository, comments_service
from app.database.db_connection import get_db
from app.users.users_service import get_current_user

router = APIRouter(prefix="/comments", tags=["comments"])


@router.post("/post/{post_id}", response_model=CommentOut)
def add_comment(post_id: int, payload: CommentCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    comments_service.ensure_post_exists(db, post_id)
    c = comments_repository.create_comment(db, user_id=current_user.id, post_id=post_id, content=payload.content)
    return c


@router.get("/post/{post_id}")
def list_comments(post_id: int, limit: int = Query(20, ge=1, le=50), offset: int = Query(0, ge=0),
                  db: Session = Depends(get_db)):
    comments_service.ensure_post_exists(db, post_id)
    limit, offset = clamp_pagination(limit, offset)
    items, total = comments_repository.list_comments_for_post(db, post_id=post_id, limit=limit, offset=offset)
    return {
        "items": [CommentOut.model_validate(c) for c in items],
        "limit": limit,
        "offset": offset,
        "total": total,
    }
