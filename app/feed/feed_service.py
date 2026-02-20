from typing import List, Tuple

from sqlalchemy.orm import Session
from sqlalchemy import desc, func

from app.database.models import Post
from app.social.follow_repository import list_following_ids


def get_feed_posts(db: Session, user_id: int, limit: int, offset: int) -> Tuple[List[Post], int]:
    following_ids = list_following_ids(db, follower_id=user_id)
    # include own posts
    user_ids = following_ids + [user_id]
    total = db.query(func.count(Post.id)).filter(Post.user_id.in_(user_ids)).scalar() or 0
    items = (
        db.query(Post)
        .filter(Post.user_id.in_(user_ids))
        .order_by(desc(Post.created_at))
        .limit(limit)
        .offset(offset)
        .all()
    )
    return items, total
