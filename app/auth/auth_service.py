from typing import Optional, Tuple

import bcrypt
from sqlalchemy.orm import Session

from app.auth import auth_repository
from app.common.exceptions import bad_request, unauthorized
from app.auth.jwt_utils import create_access_token
from app.database.models import User


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except Exception:
        return False


def register(db: Session, username: str, email: str, password: str) -> User:
    if auth_repository.get_user_by_username(db, username):
        raise bad_request("Username deja folosit")
    if auth_repository.get_user_by_email(db, email):
        raise bad_request("Email deja folosit")
    user = auth_repository.create_user(db, username=username, email=email, password_hash=hash_password(password))
    return user


def login(db: Session, username_or_email: str, password: str) -> Tuple[str, User]:
    user: Optional[User] = auth_repository.get_user_by_username(db, username_or_email)         or auth_repository.get_user_by_email(db, username_or_email)
    if not user or not verify_password(password, user.password_hash):
        raise unauthorized("Date de autentificare invalide")
    token = create_access_token(subject=str(user.id))
    return token, user
