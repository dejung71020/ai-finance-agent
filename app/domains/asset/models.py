# app/domains/asset/models.py
import enum
from sqlalchemy import Column, String, DECIMAL, DateTime, Enum, ForeignKey, Boolean, text
from sqlalchemy.dialects.postgresql import UUID
# from pgvector.sqlalchemy import Vector
from datetime import datetime
from app.core.database import Base

class AssetType(str, enum.Enum):
    DEPOSIT         = "deposit"         # 예금/적금
    SECURITIES      = "securities"      # 증권
    CRYPTO          = "crypto"          # 가상자산
    REAL_ESTATE     = "real_estate"     # 부동산
    POINTS          = "points"          # 포인트/마일리지
    CASH     = "cash"            # 현금

class Asset(Base):
    __tablename__ = "assets"
    # 금융 데이터 보안 및 확장을 위해 UUID 사용
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)

    name = Column(String, nullable=False)                   # 계좌 별명
    institution = Column(String, nullable=False)            # 기관 이름
    account_number = Column(String)                         # 계좌 번호
    asset_type = Column(Enum(AssetType), nullable=False)     # 자산 유형
    balance = Column(DECIMAL(18, 2), default=0)             # 현재 잔액
    currency = Column(String(10), default="KRW")            # 화폐 단위
    is_active = Column(Boolean, default=True)               # 연결 활성 여부

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)