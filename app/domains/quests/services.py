# Path: app/domains/quests/services.py
from sqlalchemy.orm import Session
from .repository import QuestsRepository

class QuestsService:
    def __init__(self, db: Session):
        self.repo = QuestsRepository(db)
        
    # WP 관련 핵심 비즈니스 로직 구현 위치