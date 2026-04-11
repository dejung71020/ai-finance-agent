# app/core/event_bus.py
import json
import logging
from typing import Optional

from app.core.cache import redis_client
from app.core.events.schemas import EventEnvelope

logger = logging.getLogger(__name__)

# 스트림별 최대 메시지 보존 수 [0.2.3] - [6.2] 스트림별 보존 정책
_STREAM_MAXLEN: dict[str, Optional[int]] = {
    "finance:transactions": 100_000,
    "finance:assets":       50_000,
    "finance:users":        10_000,
    "finance:automation":  50_000,
    "finance:dlq":          None,
}
_DEFAULT_MAXLEN = 20_000

class EventBus:
    async def publish(self, stream: str, event: EventEnvelope) -> Optional[str]:
        """
        이벤트 발행 -> Redis XADD 
        반드시 DB 커밋 성공후 호출하는 함수
        """
        if not redis_client.redis:
            logger.warning("Redis 미연결 — 이벤트 발행 스킵: %s", event.event_type)
            return None
        
        fields = {
            "event_id": str(event.event_id),
            "event_type": event.event_type,
            "event_version": event.event_version,
            "occurred_at": event.occurred_at.isoformat(),
            "source_domain": event.source_domain,
            "user_id": str(event.user_id) if event.user_id else "",
            "payload": json.dumps(event.payload, ensure_ascii=False),
        }

        maxlen = _STREAM_MAXLEN.get(stream, _DEFAULT_MAXLEN)
        
        # Redis stream에 데이터를 추가, 최대길이 제한
        msg_id = await redis_client.redis.xadd(
            stream,
            fields,
            maxlen=maxlen,
            approximate=True,   # [0.2.3] - [6.2] Redis 7.0 이상에서 approximate 옵션 사용 가능, 최대 길이 제한을 대략적으로 적용하여 성능 향상
        )
        logger.debug("이벤트 발행: %s → %s [%s]", event.event_type, stream, msg_id)
        return msg_id
    
    async def init_streams(self) -> None:
        """
        서버 시작 시 8개 스트림 초기화.
        스트림이 없으면 XADD로 생성하고, init 메시지 제거
        """
        if not redis_client.redis:
            logger.warning("REDIS 미연결 - 스트림 초기화 스킵")
            return
    
        streams = [
            "finance:transactions",
            "finance:assets",
            "finance:users",
            "finance:automation",
            "finance:investment",
            "finance:coach",
            "finance:planning",
            "finance:dlq",
        ]

        for stream in streams:
            try:
                exists = await redis_client.redis.exists(stream)
                if not exists:    
                    # 스트림 생성 후 init 메시지 즉시 삭제
                    msg_id = await redis_client.redis.xadd(stream, {"_init": "1"})
                    await redis_client.redis.xdel(stream, msg_id)
                    logger.info("스트림 생성 : %s", stream)
                else:
                    logger.debug("스트림 이미 존재 : %s", stream)
            except Exception as e:
                logger.error("스트림 초기화 실패 : (%s): %s", stream, e)

event_bus = EventBus()        
            