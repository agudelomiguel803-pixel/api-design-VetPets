from fastapi import APIRouter
from app.routers.cite import router as cite_router
from app.routers.treatment import router as treatment_router
from app.routers.veterinarians import router as veterinarians_router 

api_router = APIRouter()
api_router.include_router(cite_router)
api_router.include_router(treatment_router)
api_router.include_router(veterinarians_router)                      