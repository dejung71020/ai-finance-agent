# Path: app/domains/automation/router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from .services import AutomationService
from .schemas import AutomationRead

router = APIRouter(prefix='/automation', tags=['Automation'])

@router.get("/{id}", response_model=AutomationRead)
def get_automation(id, db: Session = Depends(get_db)):
    service = AutomationService(db)
    result = service.repo.get_by_id(id)
    if not result:
        raise HTTPException(status_code=404, detail="Not Found")
    return result