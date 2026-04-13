# app/api/router.py

from fastapi import APIRouter

from app.domains.planning.router import router as planning_router
from app.domains.automation.router import router as automation_router
from app.domains.investment.router import router as investment_router
from app.domains.coach.router import router as coach_router
from app.domains.transaction.router import router as transactions_router
from app.domains.assets.router import router as assets_router
from app.domains.users.router import router as users_router

router = APIRouter(prefix="/api")

# --- ROUTERS START ---
router.include_router(users_router)
router.include_router(assets_router)
router.include_router(transactions_router)
router.include_router(coach_router)
router.include_router(investment_router)
router.include_router(automation_router)
router.include_router(planning_router)
# --- ROUTERS END ---