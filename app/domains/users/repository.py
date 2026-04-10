# app/domains/users/repository.py
from sqlalchemy.orm import Session
from uuid import UUID
from .models import User

class UsersRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, obj_id: UUID):
        return self.db.query(User).filter(User.id == obj_id).first()
    
    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()
