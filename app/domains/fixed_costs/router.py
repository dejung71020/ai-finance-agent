# Path: app/domains/fixed_costs/router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from .services import FixedCostsService
from .schemas import FixedCostsRead

router = APIRouter(prefix='/fixed_costs', tags=['FixedCosts'])

@router.get("/{id}", response_model=FixedCostsRead)
def get_fixed_costs(id, db: Session = Depends(get_db)):
    service = FixedCostsService(db)
    result = service.repo.get_by_id(id)
    if not result:
        raise HTTPException(status_code=404, detail="Not Found")
    return result