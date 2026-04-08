# Path: app/domains/transactions/router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from .services import TransactionsService
from .schemas import TransactionsRead

router = APIRouter(prefix='/transactions', tags=['Transactions'])

@router.get("/{id}", response_model=TransactionsRead)
def get_transactions(id, db: Session = Depends(get_db)):
    service = TransactionsService(db)
    result = service.repo.get_by_id(id)
    if not result:
        raise HTTPException(status_code=404, detail="Not Found")
    return result