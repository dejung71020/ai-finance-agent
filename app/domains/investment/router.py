# Path: app/domains/investment/router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from .services import InvestmentService
from .schemas import InvestmentRead

router = APIRouter(prefix='/investment', tags=['Investment'])

@router.get("/{id}", response_model=InvestmentRead)
def get_investment(id, db: Session = Depends(get_db)):
    service = InvestmentService(db)
    result = service.repo.get_by_id(id)
    if not result:
        raise HTTPException(status_code=404, detail="Not Found")
    return result