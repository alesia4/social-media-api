from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth.jwt_utils import decode_token
from app.common.exceptions import unauthorized, not_found
from app.database.db_connection import get_db
from app.users import users_repository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = decode_token(token)
        user_id = int(payload.get("sub"))
    except Exception:
        raise unauthorized("Token invalid sau expirat")
    user = users_repository.get_by_id(db, user_id)
    if not user:
        raise unauthorized("User inexistent")
    return user


def get_user_or_404(db: Session, user_id: int):
    user = users_repository.get_by_id(db, user_id)
    if not user:
        raise not_found("User not found")
    return user
