# app/core/events/schemas.py
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from typing import Any, Optional

class EventEnvelope(BaseModel):
    # 메타데이터
    event_id: UUID = Field(default_factory=uuid4)   # 중복 처리 방지 키    
    event_type: str                                 # transaction.transaction.created
    event_version: str = "1.0"                      # 이벤트 스키마 버전 
    occurred_at: datetime = Field(default_factory=datetime.utcnow)

    # 라우팅
    source_domain: str                              # transaction
    user_id: Optional[UUID] = None                  # 파티셔닝 키
    correlation_id: Optional[UUID] = None           # 요청 추적용

    # 페이로드
    payload: dict[str, Any]

    # 재시도 메타
    retry_count: int = 0
    last_error: Optional[str] = None