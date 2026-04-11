# app/domains/users/repository.py
from sqlalchemy.orm import Session
from uuid import UUID
from .models import User
from typing import Union

class UsersRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, obj_id: Union[UUID, str]):
        return self.db.query(User).filter(User.id == obj_id).first()
    
    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def create(self, email: str, name: str, hashed_password: str, phone: str = None) -> User:
        user = User(
            email=email,
            name=name,
            hashed_password=hashed_password,
            phone=phone,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user