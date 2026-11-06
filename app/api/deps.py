# app/api/deps.py
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.repositories import AppointmentRepository

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_appointment_repository(session: SessionDep) -> AppointmentRepository:
    """Instancia AppointmentRepository con la sesión de BD activa."""
    return AppointmentRepository(session)