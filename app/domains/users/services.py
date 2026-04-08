# Path: app/domains/users/services.py
from sqlalchemy.orm import Session
from .repository import UsersRepository

class UsersService:
    def __init__(self, db: Session):
        self.repo = UsersRepository(db)
        
    # WP 관련 핵심 비즈니스 로직 구현 위치