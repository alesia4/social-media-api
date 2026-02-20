from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.common.exceptions import not_found, forbidden, bad_request
from app.posts import posts_repository


def get_post_or_404(db: Session, post_id: int):
    post = posts_repository.get_post(db, post_id)
    if not post:
        raise not_found("Post not found")
    return post


def delete_post(db: Session, post_id: int, current_user_id: int):
    post = get_post_or_404(db, post_id)
    if post.user_id != current_user_id:
        raise forbidden("Nu poți șterge postarea altcuiva")
    posts_repository.delete_post(db, post)


def like_post(db: Session, post_id: int, current_user_id: int):
    _ = get_post_or_404(db, post_id)
    try:
        posts_repository.add_like(db, user_id=current_user_id, post_id=post_id)
    except IntegrityError:
        db.rollback()
        # already liked
        pass
    except Exception:
        db.rollback()
        raise bad_request("Nu s-a putut da like")


def unlike_post(db: Session, post_id: int, current_user_id: int):
    _ = get_post_or_404(db, post_id)
    posts_repository.remove_like(db, user_id=current_user_id, post_id=post_id)
