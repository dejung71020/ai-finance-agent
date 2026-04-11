 # app/domains/users/services.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth import hash_password, verify_password
from .repository import UsersRepository
from .schemas import UsersCreate


class UsersService:
    def __init__(self, db: Session):
        self.repo = UsersRepository(db)

    def create_user(self, data: UsersCreate):
        if self.repo.get_by_email(data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="이미 사용 중인 이메일",
            )
        return self.repo.create(
            email=data.email,
            name=data.name,
            hashed_password=hash_password(data.password),
            phone=data.phone,
        )

    def authenticate_user(self, email: str, password: str):
        user = self.repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="이메일 또는 비밀번호가 올바르지 않습니다",
            )
        return user