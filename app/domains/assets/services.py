# Path: app/domains/assets/services.py
from sqlalchemy.orm import Session
from .repository import AssetsRepository

class AssetsService:
    def __init__(self, db: Session):
        self.repo = AssetsRepository(db)
        
    # WP 관련 핵심 비즈니스 로직 구현 위치