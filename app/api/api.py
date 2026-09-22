from fastapi import APIRouter
from .routes.academy_routes import router as academy_router

api_router = APIRouter()
api_router.include_router(academy_router, prefix="/academy", tags=["Academy"])