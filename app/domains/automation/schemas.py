# Path: app/domains/automation/schemas.py
from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class AutomationBase(BaseModel):
    pass

class AutomationCreate(AutomationBase):
    pass

class AutomationRead(AutomationBase):
    id: UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)