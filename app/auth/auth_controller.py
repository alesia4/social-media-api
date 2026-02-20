from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.common.dto import UserCreate, UserLogin, TokenOut, UserOut
from app.database.db_connection import get_db
from app.auth import auth_service
from app.users.users_service import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    return auth_service.register(
        db,
        username=payload.username,
        email=payload.email,
        password=payload.password
    )


@router.post("/login", response_model=TokenOut)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    token, _user = auth_service.login(
        db,
        username_or_email=payload.username_or_email,
        password=payload.password
    )
    return TokenOut(access_token=token)


# 👇 👇 👇  ADAUGĂ ASTA (pentru Swagger Authorize)
@router.post("/token", response_model=TokenOut)
def token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    token, _user = auth_service.login(
        db,
        username_or_email=form_data.username,
        password=form_data.password
    )
    return TokenOut(access_token=token)


@router.get("/me", response_model=UserOut)
def me(current_user=Depends(get_current_user)):
    return current_user
