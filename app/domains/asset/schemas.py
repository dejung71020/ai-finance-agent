# app/domains/asset/schemas.py
from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from decimal import Decimal
from typing import Optional

from app.domains.asset.models import AssetType

class AssetBase(BaseModel):
    name: str
    institution: str
    asset_type: AssetType
    account_number: Optional[str] = None
    balance: Decimal = Decimal("0")
    currency: str = "KRW"

class AssetCreate(AssetBase):
    pass

class AssetRead(AssetBase):
    id: UUID
    user_id: UUID
    is_active: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)