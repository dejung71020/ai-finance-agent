# Path: app/domains/automation/services.py
from sqlalchemy.orm import Session
from .repository import AutomationRepository

class AutomationService:
    def __init__(self, db: Session):
        self.repo = AutomationRepository(db)
        
    # WP 관련 핵심 비즈니스 로직 구현 위치