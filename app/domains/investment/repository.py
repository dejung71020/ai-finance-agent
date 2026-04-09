# Path: app/domains/investment/repository.py
from sqlalchemy.orm import Session
from uuid import UUID
from .models import Investment

class InvestmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, obj_id: UUID):
        return self.db.query(Investment).filter(Investment.id == obj_id).first()