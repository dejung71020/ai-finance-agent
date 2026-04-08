# Path: app/domains/users/router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from .services import UsersService
from .schemas import UsersRead

router = APIRouter(prefix='/users', tags=['Users'])

@router.get("/{id}", response_model=UsersRead)
def get_users(id, db: Session = Depends(get_db)):
    service = UsersService(db)
    result = service.repo.get_by_id(id)
    if not result:
        raise HTTPException(status_code=404, detail="Not Found")
    return result