# app/domains/users/router.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import create_access_token, create_refresh_token, get_current_user
from .services import UsersService
from .schemas import UsersCreate, UsersRead, TokenResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", response_model=UsersRead, status_code=201)
def register(data: UsersCreate, db: Session = Depends(get_db)):
    return UsersService(db).create_user(data)


@router.post("/login", response_model=TokenResponse)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm은 username/password 필드를 받음 (username = 이메일)
    user = UsersService(db).authenticate_user(form.username, form.password)
    return TokenResponse(
        access_token=create_access_token(str(user.id)),
        refresh_token=create_refresh_token(str(user.id)),
    )


@router.get("/me", response_model=UsersRead)
def get_me(current_user=Depends(get_current_user)):
    return current_user


@router.get("/{id}", response_model=UsersRead)
def get_user(id: str, db: Session = Depends(get_db)):
    service = UsersService(db)
    result = service.repo.get_by_id(id)
    if not result:
        raise HTTPException(status_code=404, detail="Not Found")
    return result