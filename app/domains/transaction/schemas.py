# app/domains/transaction/schemas.py
from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from decimal import Decimal
from typing import Optional
from app.domains.transaction.models import TransactionType

class TransactionBase(BaseModel):
    asset_id:           UUID
    amount:             Decimal
    transaction_type:   TransactionType
    category:           Optional[str] = None
    description:        Optional[str] = None
    merchant:           Optional[str] = None
    transacted_at:      datetime

class TransactionCreate(TransactionBase):
    pass

class TransactionRead(TransactionBase):
    id:             UUID
    user_id:        UUID
    created_at:     datetime
    model_config = ConfigDict(from_attributes=True)