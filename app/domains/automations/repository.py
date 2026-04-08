# Path: app/domains/automations/repository.py
from sqlalchemy.orm import Session
from uuid import UUID
from .models import Automations

class AutomationsRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, obj_id: UUID):
        return self.db.query(Automations).filter(Automations.id == obj_id).first()