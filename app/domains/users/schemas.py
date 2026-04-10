# app/domains/users/schemas.py
from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class UsersBase(BaseModel):
    email: str
    name: str
    phone: Optional[str] = None

class UsersCreate(UsersBase):
    password: str

class UsersRead(UsersBase):
    id: UUID
    is_active: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)