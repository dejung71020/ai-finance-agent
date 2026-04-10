# Path: app/core/database.py
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

logger = logging.getLogger(__name__)

try:
    engine = create_engine(
        settings.POSTGRESQL_URL,
        pool_size=10,           # 기본으로 10개 연결 유지
        max_overflow=20,        # 최대 20개 추가 연결 허용
        pool_recycle=3600,      # 1시간마다 연결 재시작
        pool_pre_ping=True,     # 연결 확인 후 사용
        echo=settings.DEBUG     # 디버그 모드일때만 SQL 로그 출력
    )
    logger.info("데이터베이스 엔진 생성 성공")
except Exception as e:
    logger.error(f"데이터베이스 엔진 생성 실패 : {str(e)}")
    raise

SessionLocal = sessionmaker(autocommit=False, authoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()