# Path: app/domains/planning/router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from .services import PlanningService
from .schemas import PlanningRead

router = APIRouter(prefix='/planning', tags=['Planning'])

@router.get("/{id}", response_model=PlanningRead)
def get_planning(id, db: Session = Depends(get_db)):
    service = PlanningService(db)
    result = service.repo.get_by_id(id)
    if not result:
        raise HTTPException(status_code=404, detail="Not Found")
    return result