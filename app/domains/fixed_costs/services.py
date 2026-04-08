# Path: app/domains/fixed_costs/services.py
from sqlalchemy.orm import Session
from .repository import FixedCostsRepository

class FixedCostsService:
    def __init__(self, db: Session):
        self.repo = FixedCostsRepository(db)
        
    # WP 관련 핵심 비즈니스 로직 구현 위치