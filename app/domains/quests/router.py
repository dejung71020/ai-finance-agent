# Path: app/domains/quests/router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from .services import QuestsService
from .schemas import QuestsRead

router = APIRouter(prefix='/quests', tags=['Quests'])

@router.get("/{id}", response_model=QuestsRead)
def get_quests(id, db: Session = Depends(get_db)):
    service = QuestsService(db)
    result = service.repo.get_by_id(id)
    if not result:
        raise HTTPException(status_code=404, detail="Not Found")
    return result