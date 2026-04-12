# Path: app/domains/assets/router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.core.auth import get_current_user
from .services import AssetsService
from .schemas import AssetsRead, AssetsCreate

router = APIRouter(prefix='/assets', tags=['Assets'])


@router.post("", response_model=AssetsRead, status_code=201)
def create_asset(
    data: AssetsCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return AssetsService(db).create_asset(current_user.id, data)
    
@router.get("", response_model=list[AssetsRead])
def get_my_assets(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return AssetsService(db).get_my_assets(current_user.id)


@router.get("/{id}", response_model=AssetsRead)
def get_assets(
    id: UUID, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
    ):
    return AssetsService(db).get_asset(current_user.id, id)

@router.delete("/{id}", status_code=204)
def delete_asset(
    id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    AssetsService(db).delete_asset(current_user.id, id)