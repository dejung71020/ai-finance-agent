# Path: app/domains/assets/repository.py
from sqlalchemy.orm import Session
from uuid import UUID
from .models import Asset

class AssetsRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, obj_id: UUID):
        return self.db.query(Asset).filter(Asset.id == obj_id).first()