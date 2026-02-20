from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.common.dto import PostCreate, PostOut, FeedOut
from app.database.db_connection import get_db
from app.posts import posts_repository, posts_service
from app.users.users_service import get_current_user
from app.common.utils import clamp_pagination

router = APIRouter(prefix="/posts", tags=["posts"])


def _to_post_out(db: Session, post) -> PostOut:
    return PostOut(
        id=post.id,
        user_id=post.user_id,
        content=post.content,
        image_url=post.image_url,
        created_at=post.created_at,
        likes_count=posts_repository.likes_count(db, post.id),
        comments_count=posts_repository.comments_count(db, post.id),
    )


@router.post("/", response_model=PostOut)
def create_post(payload: PostCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    post = posts_repository.create_post(db, user_id=current_user.id, content=payload.content, image_url=payload.image_url)
    return _to_post_out(db, post)


@router.get("/user/{user_id}", response_model=FeedOut)
def list_user_posts(user_id: int, limit: int = Query(20, ge=1, le=50), offset: int = Query(0, ge=0),
                    db: Session = Depends(get_db)):
    limit, offset = clamp_pagination(limit, offset)
    posts, total = posts_repository.list_posts_by_user(db, user_id=user_id, limit=limit, offset=offset)
    return FeedOut(items=[_to_post_out(db, p) for p in posts], limit=limit, offset=offset, total=total)


@router.get("/{post_id}", response_model=PostOut)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = posts_service.get_post_or_404(db, post_id)
    return _to_post_out(db, post)


@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    posts_service.delete_post(db, post_id=post_id, current_user_id=current_user.id)
    return {"status": "deleted"}


@router.post("/{post_id}/like")
def like(post_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    posts_service.like_post(db, post_id=post_id, current_user_id=current_user.id)
    return {"status": "liked"}


@router.delete("/{post_id}/like")
def unlike(post_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    posts_service.unlike_post(db, post_id=post_id, current_user_id=current_user.id)
    return {"status": "unliked"}
