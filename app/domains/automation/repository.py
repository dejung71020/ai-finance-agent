# Path: app/domains/automation/repository.py
from sqlalchemy.orm import Session
from uuid import UUID
from .models import Automation

class AutomationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, obj_id: UUID):
        return self.db.query(Automation).filter(Automation.id == obj_id).first()