from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scalar_fastapi import get_scalar_api_reference

from app.core.config import settings
from app.core.database import init_db
from app.routers import api_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Ciclo de vida de la aplicación: crea las tablas de la BD al arrancar."""
    await init_db()
    yield


app = FastAPI(
    title=f"{settings.PROJECT_NAME} - API VetPets",
    version=settings.VERSION,
    description="API de VetPets para gestión de mascotas, veterinarios, citas y tratamientos.",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# --- CONFIGURACIÓN DE CORS PARA EL FRONTEND (VITE) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- INCLUIR LAS RUTAS DE LOS ROUTERS ---
app.include_router(api_router, prefix="/api/v1")


@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    """Endpoint para comprobación del estado del servicio."""
    return {"status": "healthy", "service": "vetpets-api"}


@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    """Interfaz interactiva de documentación y pruebas con Scalar."""
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )