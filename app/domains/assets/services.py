# app/domains/assets/services.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.encryption import encrypt
from .repository import AssetsRepository
from .schemas import AssetsCreate

class AssetsService:
    def __init__(self, db: Session):
        self.repo = AssetsRepository(db)
        
    def create_asset(self, user_id: UUID, data: AssetsCreate):
        return self.repo.create(
            user_id=user_id,
            name=data.name,
            institution=data.institution,
            asset_type=data.asset_type,
            account_number=encrypt(data.account_number) if data.account_number else None,
            balance=data.balance,
            currency=data.currency,
        )
    
    def get_my_assets(self, user_id: UUID):
        return self.repo.get_by_user_id(user_id)
    
    def get_asset(self, user_id: UUID, asset_id: UUID):
        asset = self.repo.get_by_id(asset_id)
        if not asset or asset.user_id != user_id:
            raise HTTPException(status_code=404, detail="Not Found")
        return asset
    
    def delete_asset(self, user_id: UUID, asset_id: UUID):
        asset = self.repo.get_by_id(asset_id)
        if not asset or asset.user_id != user_id:
            raise HTTPException(status_code=404, detail="Not Found")
        self.repo.delete(asset_id)