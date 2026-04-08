# Path: app/domains/users/schemas.py
from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class UsersBase(BaseModel):
    pass

class UsersCreate(UsersBase):
    pass

class UsersRead(UsersBase):
    id: UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)