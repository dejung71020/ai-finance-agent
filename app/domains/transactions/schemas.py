# Path: app/domains/transactions/schemas.py
from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class TransactionsBase(BaseModel):
    pass

class TransactionsCreate(TransactionsBase):
    pass

class TransactionsRead(TransactionsBase):
    id: UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)