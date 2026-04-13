# app/domains/transaction/repository.py
from sqlalchemy.orm import Session
from uuid import UUID
from .models import Transaction

class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, transaction_id: UUID):
        return self.db.query(Transaction).filter(Transaction.id == transaction_id).first()
    
    def get_by_user_id(self, user_id: UUID) -> list[Transaction]:
        return (
            self.db.query(Transaction)
            .filter(Transaction.user_id == user_id)
            .order_by(Transaction.transacted_at.desc())
            .all()
        )
    
    def get_by_asset_id(self, user_id: UUID, asset_id: UUID) -> list[Transaction]:
        return (
            self.db.query(Transaction)
            .filter(Transaction.user_id == user_id, Transaction.asset_id == asset_id)
            .order_by(Transaction.transacted_at.desc())
            .all()
        )
    
    def create(self, user_id: UUID, data, category: str) -> Transaction:
        tx = Transaction(
            user_id = user_id,
            asset_id = data.asset_id,
            amount = data.amount,
            transaction_type = data.transaction_type,
            category = category,
            description = data.description,
            merchant = data.merchant,
            transacted_at = data.transacted_at,
        )
        self.db.add(tx)
        self.db.commit()
        self.db.refresh(tx)
        return tx
    
    def delete(self, transaction_id: UUID) -> bool:
        tx = self.get_by_id(transaction_id)
        if not tx:
            return False
        self.db.delete(tx)
        self.db.commit()
        return True