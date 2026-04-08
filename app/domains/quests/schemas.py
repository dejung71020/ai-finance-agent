# Path: app/domains/quests/schemas.py
from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class QuestsBase(BaseModel):
    pass

class QuestsCreate(QuestsBase):
    pass

class QuestsRead(QuestsBase):
    id: UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)