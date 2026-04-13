# app/domains/transaction/services.py
from fastapi import HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.event_bus import event_bus
from app.core.events.schemas import EventEnvelope
from .repository import TransactionRepository
from .schemas import TransactionCreate

class TransactionService:
    def __init__(self, db: Session):
        self.repo = TransactionRepository(db)
        
    async def create_transaction(self, user_id: UUID, data: TransactionCreate):
        tx = self.repo.create(user_id, data)

        await event_bus.publish(
            "finance:transactions",
            EventEnvelope(
                event_type="transactions.transaction.created",
                source_domain="transactions",
                user_id=user_id,
                payload={
                    "transaction_id": str(tx.id),
                    "asset_id": str(tx.asset_id),
                    "amount": str(tx.amount),
                    "transaction_type": tx.transaction_type,
                    "transacted_at": tx.transacted_at.isoformat(),
                },
            ),
        )
        return tx
    
    def get_my_transactions(self, user_id: UUID):
        return self.repo.get_by_user_id(user_id)
    
    def get_by_asset(self, user_id: UUID, asset_id: UUID):
        return self.repo.get_by_asset_id(user_id, asset_id)
    
    def get_transaction(self, user_id: UUID, transaction_id: UUID):
        tx = self.repo.get_by_id(transaction_id)
        if not tx or tx.user_id != user_id:
            raise HTTPException(status_code=404, detail="Not Found")
        return tx
    
    def delete_transaction(self, user_id: UUID, transaction_id: UUID):
        tx = self.repo.get_by_id(transaction_id)
        if not tx or tx.user_id != user_id:
            raise HTTPException(status_code=404, detail="Not Found")
        self.repo.delete(transaction_id)