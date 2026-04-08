# Path: app/domains/assets/repository.py
from sqlalchemy.orm import Session
from uuid import UUID
from .models import Assets

class AssetsRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, obj_id: UUID):
        return self.db.query(Assets).filter(Assets.id == obj_id).first()