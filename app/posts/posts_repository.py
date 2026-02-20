from typing import List, Optional, Tuple

from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.database.models import Post, Like, Comment


def create_post(db: Session, user_id: int, content: str, image_url: Optional[str]) -> Post:
    post = Post(user_id=user_id, content=content, image_url=image_url)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def get_post(db: Session, post_id: int) -> Optional[Post]:
    return db.query(Post).filter(Post.id == post_id).first()


def delete_post(db: Session, post: Post) -> None:
    db.delete(post)
    db.commit()


def list_posts_by_user(db: Session, user_id: int, limit: int, offset: int) -> Tuple[List[Post], int]:
    total = db.query(func.count(Post.id)).filter(Post.user_id == user_id).scalar() or 0
    items = (
        db.query(Post)
        .filter(Post.user_id == user_id)
        .order_by(desc(Post.created_at))
        .limit(limit)
        .offset(offset)
        .all()
    )
    return items, total


def add_like(db: Session, user_id: int, post_id: int) -> None:
    like = Like(user_id=user_id, post_id=post_id)
    db.add(like)
    db.commit()


def remove_like(db: Session, user_id: int, post_id: int) -> int:
    q = db.query(Like).filter(Like.user_id == user_id, Like.post_id == post_id)
    deleted = q.delete()
    db.commit()
    return deleted


def likes_count(db: Session, post_id: int) -> int:
    return db.query(func.count(Like.post_id)).filter(Like.post_id == post_id).scalar() or 0


def comments_count(db: Session, post_id: int) -> int:
    return db.query(func.count(Comment.id)).filter(Comment.post_id == post_id).scalar() or 0
