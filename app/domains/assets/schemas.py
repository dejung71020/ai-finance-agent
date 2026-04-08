# Path: app/domains/assets/schemas.py
from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class AssetsBase(BaseModel):
    pass

class AssetsCreate(AssetsBase):
    pass

class AssetsRead(AssetsBase):
    id: UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)