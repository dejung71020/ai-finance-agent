# Path: app/main.py
import logging

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.config import settings
from app.core.database import get_db
from app.core.lifespan import lifespan
from app.api.router import router

logging.basicConfig(level=logging.INFO if not settings.DEBUG else logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="개인화 AI 금융 비서 (Finance OS) API",
    version=settings.VERSION,
    lifespan=lifespan
)

@app.get("/")
def health_check():
    return {
        "status": "running",
        "project": settings.PROJECT_NAME
        }

@app.get("health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "project": settings.PROJECT_NAME,
            "database": "연결됨"
        }
    except Exception as e:
        logger.error(f"DB 연결 실패: {str(e)}")
        raise HTTPException(status_code=503, detail="DB 연결 실패")

app.include_router(router)