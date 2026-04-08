# Path: app/domains/quests/repository.py
from sqlalchemy.orm import Session
from uuid import UUID
from .models import Quests

class QuestsRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, obj_id: UUID):
        return self.db.query(Quests).filter(Quests.id == obj_id).first()