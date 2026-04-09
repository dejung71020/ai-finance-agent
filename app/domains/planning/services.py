# Path: app/domains/planning/services.py
from sqlalchemy.orm import Session
from .repository import PlanningRepository

class PlanningService:
    def __init__(self, db: Session):
        self.repo = PlanningRepository(db)
        
    # WP 관련 핵심 비즈니스 로직 구현 위치