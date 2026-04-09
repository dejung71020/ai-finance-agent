# Path: app/domains/coach/services.py
from sqlalchemy.orm import Session
from .repository import CoachRepository

class CoachService:
    def __init__(self, db: Session):
        self.repo = CoachRepository(db)
        
    # WP 관련 핵심 비즈니스 로직 구현 위치