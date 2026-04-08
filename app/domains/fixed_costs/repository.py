# Path: app/domains/fixed_costs/repository.py
from sqlalchemy.orm import Session
from uuid import UUID
from .models import FixedCosts

class FixedCostsRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, obj_id: UUID):
        return self.db.query(FixedCosts).filter(FixedCosts.id == obj_id).first()