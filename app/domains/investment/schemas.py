# Path: app/domains/investment/schemas.py
from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class InvestmentBase(BaseModel):
    pass

class InvestmentCreate(InvestmentBase):
    pass

class InvestmentRead(InvestmentBase):
    id: UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)