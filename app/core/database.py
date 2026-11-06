from collections.abc import AsyncGenerator
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import make_url
from sqlmodel import SQLModel

from app.core.config import settings

# 1. Parseamos la URL de la base de datos
url = make_url(settings.DATABASE_URL)

# 2. Aseguramos que el driver sea postgresql+asyncpg si apunta a postgres
if url.drivername in ["postgres", "postgresql"]:
    url = url.set(drivername="postgresql+asyncpg")

# 3. Limpiamos los parámetros de la URL que asyncpg no acepta directamente
query = dict(url.query)
query.pop("sslmode", None)
query.pop("channel_binding", None)
url = url.set(query=query)

# Argumentos de conexión especiales (Neon / asyncpg)
connect_args: dict[str, Any] = {}
if "neon.tech" in settings.DATABASE_URL:
    # Neon exige SSL para conexiones externas con asyncpg
    connect_args["ssl"] = "require"
    if "pooler" in settings.DATABASE_URL:
        connect_args["statement_cache_size"] = 0

# Motor asíncrono compatible con Neon PostgreSQL
engine = create_async_engine(
    url,
    echo=settings.ECHO_SQL,
    pool_pre_ping=True,
    connect_args=connect_args,
    future=True,
)

# Fábrica de sesiones asíncronas
async_session_maker = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

async def init_db() -> None:
    """Crea las tablas en la base de datos si no existen."""
    import app.models  # noqa: F401

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependencia de FastAPI para obtener la sesión de base de datos."""
    async with async_session_maker() as session:
        yield session