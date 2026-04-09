# Path: app/domains/coach/repository.py
from sqlalchemy.orm import Session
from uuid import UUID
from .models import Coach

class CoachRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, obj_id: UUID):
        return self.db.query(Coach).filter(Coach.id == obj_id).first()