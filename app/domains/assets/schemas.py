# app/domains/assets/schemas.py
from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from decimal import Decimal
from typing import Optional

from app.domains.assets.models import AssetType

class AssetsBase(BaseModel):
    name: str
    institution: str
    asset_type: AssetType
    account_number: Optional[str] = None
    balance: Decimal = Decimal("0")
    currency: str = "KRW"

class AssetsCreate(AssetsBase):
    pass

class AssetsRead(AssetsBase):
    id: UUID
    user_id: UUID
    is_active: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)