# Path: app/domains/users/repository.py
from sqlalchemy.orm import Session
from uuid import UUID
from .models import Users

class UsersRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, obj_id: UUID):
        return self.db.query(Users).filter(Users.id == obj_id).first()