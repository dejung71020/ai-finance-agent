# app/domains/users/models.py
from sqlalchemy import Column, String, DECIMAL, DateTime, ForeignKey, Boolean, text
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    # 금융 데이터 보안 및 확장을 위해 UUID 사용
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    email = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    phone = Column(String) # AES-256 암호화 0.3.3
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)