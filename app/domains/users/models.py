# Path: app/domains/users/models.py
from sqlalchemy import Column, String, DECIMAL, DateTime, ForeignKey, Boolean, text
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
from datetime import datetime
from app.core.database import Base

class Users(Base):
    __tablename__ = "userss"
    # 금융 데이터 보안 및 확장을 위해 UUID 사용
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    
    # 💡 도메인별 컬럼을 아래에 추가하세요
    # 예: user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)