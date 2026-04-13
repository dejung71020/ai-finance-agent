# app/domains/transaction/models.py
import enum
from sqlalchemy import Column, String, DECIMAL, DateTime, Enum, ForeignKey, Boolean, Text, text
from sqlalchemy.dialects.postgresql import UUID
# from pgvector.sqlalchemy import Vector
from datetime import datetime
from app.core.database import Base

class TransactionType(str, enum.Enum):
    INCOME      = "income"      # 수입
    EXPENSE     = "expense"     # 지출
    TRANSFER    = "transfer"    # 이체

class Transaction(Base):
    '''
    거래 ID
    사용자 ID
    asset ID
    양
    거래 타입
    사용 용도
    설명
    가맹정, 상호명
    실제 거래 일시
    등록 일시
    '''
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False, index=True)

    amount = Column(DECIMAL(18, 2), nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    category = Column(String(50))

    description = Column(Text)
    merchant = Column(String(100))
    transacted_at = Column(DateTime, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)