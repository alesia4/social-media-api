from typing import List, Tuple

from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.database.models import Comment


def create_comment(db: Session, user_id: int, post_id: int, content: str) -> Comment:
    c = Comment(user_id=user_id, post_id=post_id, content=content)
    db.add(c)
    db.commit()
    db.refresh(c)
    return c


def list_comments_for_post(db: Session, post_id: int, limit: int, offset: int) -> Tuple[List[Comment], int]:
    total = db.query(func.count(Comment.id)).filter(Comment.post_id == post_id).scalar() or 0
    items = (
        db.query(Comment)
        .filter(Comment.post_id == post_id)
        .order_by(desc(Comment.created_at))
        .limit(limit)
        .offset(offset)
        .all()
    )
    return items, total
