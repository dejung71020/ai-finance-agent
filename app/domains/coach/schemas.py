# Path: app/domains/coach/schemas.py
from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class CoachBase(BaseModel):
    pass

class CoachCreate(CoachBase):
    pass

class CoachRead(CoachBase):
    id: UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)