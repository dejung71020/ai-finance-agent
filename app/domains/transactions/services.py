# Path: app/domains/transactions/services.py
from sqlalchemy.orm import Session
from .repository import TransactionsRepository

class TransactionsService:
    def __init__(self, db: Session):
        self.repo = TransactionsRepository(db)
        
    # WP 관련 핵심 비즈니스 로직 구현 위치