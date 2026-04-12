# Path: app/domains/transactions/repository.py
from sqlalchemy.orm import Session
from uuid import UUID
from .models import Transaction

class TransactionsRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, obj_id: UUID):
        return self.db.query(Transaction).filter(Transaction.id == obj_id).first()