from fastapi import APIRouter

from backend.app.modules.health.router import router as health_checking_router

api_router = APIRouter()
hc_api_router = APIRouter()
hc_api_router.include_router(health_checking_router, prefix="/healthz")
