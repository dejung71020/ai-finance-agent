# Path: app/domains/planning/schemas.py
from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class PlanningBase(BaseModel):
    pass

class PlanningCreate(PlanningBase):
    pass

class PlanningRead(PlanningBase):
    id: UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)