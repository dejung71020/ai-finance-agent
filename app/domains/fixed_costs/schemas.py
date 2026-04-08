# Path: app/domains/fixed_costs/schemas.py
from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class FixedCostsBase(BaseModel):
    pass

class FixedCostsCreate(FixedCostsBase):
    pass

class FixedCostsRead(FixedCostsBase):
    id: UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)