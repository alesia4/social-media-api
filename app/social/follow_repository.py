from typing import List, Tuple

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.models import Follow, User


def follow(db: Session, follower_id: int, following_id: int) -> None:
    db.add(Follow(follower_id=follower_id, following_id=following_id))
    db.commit()


def unfollow(db: Session, follower_id: int, following_id: int) -> int:
    deleted = (
        db.query(Follow)
        .filter(Follow.follower_id == follower_id, Follow.following_id == following_id)
        .delete()
    )
    db.commit()
    return deleted


def list_following_ids(db: Session, follower_id: int) -> List[int]:
    rows = db.query(Follow.following_id).filter(Follow.follower_id == follower_id).all()
    return [r[0] for r in rows]


def list_followers(db: Session, user_id: int, limit: int, offset: int) -> Tuple[List[User], int]:
    total = db.query(func.count(Follow.follower_id)).filter(Follow.following_id == user_id).scalar() or 0
    items = (
        db.query(User)
        .join(Follow, Follow.follower_id == User.id)
        .filter(Follow.following_id == user_id)
        .order_by(User.username.asc())
        .limit(limit)
        .offset(offset)
        .all()
    )
    return items, total


def list_following(db: Session, user_id: int, limit: int, offset: int) -> Tuple[List[User], int]:
    total = db.query(func.count(Follow.following_id)).filter(Follow.follower_id == user_id).scalar() or 0
    items = (
        db.query(User)
        .join(Follow, Follow.following_id == User.id)
        .filter(Follow.follower_id == user_id)
        .order_by(User.username.asc())
        .limit(limit)
        .offset(offset)
        .all()
    )
    return items, total
