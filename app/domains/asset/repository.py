# app/domains/asset/repository.py
from sqlalchemy.orm import Session
from uuid import UUID
from decimal import Decimal
from .models import Asset

class AssetRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, asset_id: UUID):
        return self.db.query(Asset).filter(Asset.id == asset_id).first()
    
    def get_by_user_id(self, user_id: UUID):
        return self.db.query(Asset).filter(
            Asset.user_id == user_id,
            Asset.is_active == True
        ).all()
    
    def create(self, 
               user_id: UUID, 
               name: str, 
               institution: str, 
               asset_type, 
               account_number: str | None,
               balance: Decimal,
               currency: str
               ) -> Asset:
        asset = Asset(
            user_id=user_id,
            name=name,
            institution=institution,
            asset_type=asset_type,
            account_number=account_number,
            balance=balance,
            currency=currency,
        )
        self.db.add(asset)
        self.db.commit()
        self.db.refresh(asset)
        return asset
    
    def update_balance(self, asset_id: UUID, balance: Decimal) -> Asset | None:
        asset = self.get_by_id(asset_id)
        if not asset:
            return None
        asset.balance = balance
        self.db.commit()
        self.db.refresh(asset)
        return asset
    
    def delete(self, asset_id: UUID) -> bool:
        asset = self.get_by_id(asset_id)
        if not asset:
            return False
        asset.is_active = False
        self.db.commit()
        return True