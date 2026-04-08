# Path: app/domains/automations/schemas.py
from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class AutomationsBase(BaseModel):
    pass

class AutomationsCreate(AutomationsBase):
    pass

class AutomationsRead(AutomationsBase):
    id: UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)