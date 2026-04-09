# Path: app/domains/investment/services.py
from sqlalchemy.orm import Session
from .repository import InvestmentRepository

class InvestmentService:
    def __init__(self, db: Session):
        self.repo = InvestmentRepository(db)
        
    # WP 관련 핵심 비즈니스 로직 구현 위치