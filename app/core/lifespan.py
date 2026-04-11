# app/core/lifespan.py
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.config import settings
from app.core.database import engine, Base
from app.core.cache import redis_client
from app.core.event_bus import event_bus

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 서버 시작 시 실행
    logger.info(f"[{settings.PROJECT_NAME}] [{settings.VERSION}] 서버 실행")

    # PostgreSQL DB 테이블 생성
    try:        
        Base.metadata.create_all(bind=engine)
        logger.info("DB 테이블 생성 완료")
    except Exception as e:
        logger.error(f"DB 테이블 생성 실패: {str(e)}")

    # Redis 연결 풀 생성, event_bus.init
    try:
        await redis_client.connect()
        await event_bus.init_streams()
    except Exception as e:
        logger.error(f"REDIS 연결 실패 : {str(e)}")

    yield

    # 서버 종료 시 실행
    logger.info("서버 종료")
    
    
    await redis_client.disconnect()
    engine.dispose()
    
    logger.info("DB 연결 종료")