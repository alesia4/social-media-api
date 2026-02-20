from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database.models import User


def get_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def get_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()


def search(db: Session, q: str, limit: int = 20) -> List[User]:
    q_like = f"%{q}%"
    return (
        db.query(User)
        .filter(or_(User.username.ilike(q_like), User.email.ilike(q_like)))
        .order_by(User.username.asc())
        .limit(limit)
        .all()
    )


def update_profile(db: Session, user: User, bio: Optional[str], avatar_url: Optional[str]) -> User:
    if bio is not None:
        user.bio = bio
    if avatar_url is not None:
        user.avatar_url = avatar_url
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
