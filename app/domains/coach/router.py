# Path: app/domains/coach/router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from .services import CoachService
from .schemas import CoachRead

router = APIRouter(prefix='/coach', tags=['Coach'])

@router.get("/{id}", response_model=CoachRead)
def get_coach(id, db: Session = Depends(get_db)):
    service = CoachService(db)
    result = service.repo.get_by_id(id)
    if not result:
        raise HTTPException(status_code=404, detail="Not Found")
    return result