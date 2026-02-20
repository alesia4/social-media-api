from sqlalchemy.orm import Session

from app.common.exceptions import not_found
from app.posts.posts_repository import get_post


def ensure_post_exists(db: Session, post_id: int):
    if not get_post(db, post_id):
        raise not_found("Post not found")
