from fastapi import APIRouter
from app.routers.cite import router as cite_router

api_router = APIRouter()
api_router.include_router(cite_router)