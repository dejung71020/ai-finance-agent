# Path: app/domains/transactions/repository.py
from sqlalchemy.orm import Session
from uuid import UUID
from .models import Transactions

class TransactionsRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, obj_id: UUID):
        return self.db.query(Transactions).filter(Transactions.id == obj_id).first()