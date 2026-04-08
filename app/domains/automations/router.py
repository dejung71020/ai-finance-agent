# Path: app/domains/automations/router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from .services import AutomationsService
from .schemas import AutomationsRead

router = APIRouter(prefix='/automations', tags=['Automations'])

@router.get("/{id}", response_model=AutomationsRead)
def get_automations(id, db: Session = Depends(get_db)):
    service = AutomationsService(db)
    result = service.repo.get_by_id(id)
    if not result:
        raise HTTPException(status_code=404, detail="Not Found")
    return result