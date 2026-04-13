# app/domains/transaction/router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.core.auth import get_current_user
from .services import TransactionService
from .schemas import TransactionCreate,TransactionRead

router = APIRouter(prefix='/transactions', tags=['Transactions'])

@router.post("", response_model=TransactionRead, status_code=201)
async def create_transaction(
    data: TransactionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    return await TransactionService(db).create_transaction(current_user.id, data)

@router.get("", response_model=list[TransactionRead])
def get_my_transactions(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    return TransactionService(db).get_my_transactions(current_user.id)

@router.get("/asset/{asset_id}", response_model=list[TransactionRead])
def get_by_asset(
    asset_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    return TransactionService(db).get_by_asset(current_user.id, asset_id)


@router.get("/{id}", response_model=TransactionRead)
def get_transaction(
    id: UUID, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    ):
    return TransactionService(db).get_transaction(current_user.id, id)

@router.delete("/{id}", status_code=204)
def delete_transaction(
    id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
): 
    return TransactionService(db).delete_transaction(current_user.id, id)