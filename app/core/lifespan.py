# app/core/lifespan.py
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.config import settings
from app.core.database import engine, Base

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 서버 시작 시 실행
    logger.info(f"[{settings.PROJECT_NAME}] [{settings.VERSION}] 서버 실행")
    try:
        # DB 테이블 생성
        Base.metadata.create_all(bind=engine)
        logger.info("DB 테이블 생성 완료")
    except Exception as e:
        logger.error(f"DB 테이블 생성 실패: {str(e)}")

    yield

    # 서버 종료 시 실행
    logger.info("서버 종료")
    engine.dispose()
    logger.info("DB 연결 종료")