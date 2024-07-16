from fastapi import APIRouter

from backend.app.modules.blog_poster.router import router as blog_poster_router
from backend.app.modules.health.router import router as health_checking_router

api_router = APIRouter()
api_router.include_router(blog_poster_router, prefix="/blog_poster")

hc_api_router = APIRouter()
hc_api_router.include_router(health_checking_router, prefix="/healthz")
