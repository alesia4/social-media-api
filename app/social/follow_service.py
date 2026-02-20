from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.common.exceptions import bad_request
from app.users.users_repository import get_by_id
from app.social import follow_repository


def follow_user(db: Session, follower_id: int, following_id: int):
    if follower_id == following_id:
        raise bad_request("Nu te poți urmări singur")
    if not get_by_id(db, following_id):
        raise bad_request("User-ul urmărit nu există")
    try:
        follow_repository.follow(db, follower_id=follower_id, following_id=following_id)
    except IntegrityError:
        db.rollback()
        # already following
        pass


def unfollow_user(db: Session, follower_id: int, following_id: int):
    follow_repository.unfollow(db, follower_id=follower_id, following_id=following_id)
