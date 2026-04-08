# Path: app/domains/assets/router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from .services import AssetsService
from .schemas import AssetsRead

router = APIRouter(prefix='/assets', tags=['Assets'])

@router.get("/{id}", response_model=AssetsRead)
def get_assets(id, db: Session = Depends(get_db)):
    service = AssetsService(db)
    result = service.repo.get_by_id(id)
    if not result:
        raise HTTPException(status_code=404, detail="Not Found")
    return result