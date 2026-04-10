# app/core/cache.py
import logging
import json
from typing import Optional, Any
from redis.asyncio import Redis, ConnectionPool
from app.core.config import settings

logger = logging.getLogger(__name__)

class RedisClient:
    def __init__(self):
        self.pool: Optional[ConnectionPool] = None
        self.redis: Optional[Redis] = None

    async def connect(self):
        """
        서버 시작 시 Redis 연결 풀 생성
        """
        if not settings.REDIS_URL:
            logger.warning("REDIS_URL이 설정되지 않았습니다.")
            return

        try:
            self.pool = ConnectionPool.from_url(
                settings.REDIS_URL,
                decode_responses=True, # bytes -> 문자열로 응답받기
                max_connections=100, # 최대 동시 커넥션 제어
                socket_timeout=5, # 소켓 타임아웃
                socket_connect_timeout=5, # 소켓 연결 타임아웃
            )

            self.redis = Redis(connection_pool=self.pool)

            # PING 테스트로 연결 확인
            await self.redis.ping()
            logger.info("REDIS 연결 풀 생성 및 연결 성공")

        except Exception as e:
            logger.error(f"Redis 연결 풀 생성 실패: {str(e)}")
            raise
    
    async def disconnect(self):
        """
        서버 종료 시 REDIS 연결 풀 반환
        """
        if self.redis:
            await self.redis.close()
        if self.pool:
            await self.pool.disconnect()
            logger.info("REDIS 연결 안전 종료")
    
    async def get(self, key: str) -> Optional[Any]:
        """
        캐시 조회 (JSON 문자열 -> Python 객체)
        """
        if not self.redis:
            return None
        
        val = await self.redis.get(key)
        if val:
            try:
                return json.loads(val)
            except json.JSONDecodeError:
                return val
        return None
    
    async def set(self, key: str, value: Any, expire: int = 3600) -> bool:
        """
        캐시 저장 (Python 객체 -> JSON 문자열)
        """
        if not self.redis:
            return False
        
        # {}, [] 는 JSON 문자열로 변환 후 저장
        val = json.dumps(value) if isinstance(value, (dict, list)) else value
        return await self.redis.set(key, val, ex=expire)

    async def delete(self, key: str) -> bool:
        """
        캐시 삭제
        """
        if not self.redis:
            return False
        return await self.redis.delete(key) > 0
    
redis_client = RedisClient()