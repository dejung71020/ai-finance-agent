from app.domains.planning.router import router as planning_router
from app.domains.automation.router import router as automation_router
from app.domains.investment.router import router as investment_router
from app.domains.coach.router import router as coach_router
from app.domains.quests.router import router as quests_router
from app.domains.automations.router import router as automations_router
from app.domains.fixed_costs.router import router as fixed_costs_router
from app.domains.transactions.router import router as transactions_router
from app.domains.assets.router import router as assets_router
from app.domains.users.router import router as users_router
# Path: app/main.py
from fastapi import FastAPI
from app.core.database import engine, Base

app = FastAPI(
    title="AI Finance Assistant API",
    description="WP 1~5 통합 금융 비서 백엔드",
    version="1.0.0"
)

# DB 테이블 생성 (최초 실행 시)
Base.metadata.create_all(bind=engine)

@app.get("/")
def health_check():
    return {"status": "running", "project": "AI Finance Assistant"}

# --- [자동 라우터 연동 영역] ---
# --- ROUTERS START ---
app.include_router(users_router)
app.include_router(assets_router)
app.include_router(transactions_router)
app.include_router(fixed_costs_router)
app.include_router(automations_router)
app.include_router(quests_router)
app.include_router(coach_router)
app.include_router(investment_router)
app.include_router(automation_router)
app.include_router(planning_router)
# --- ROUTERS END ---