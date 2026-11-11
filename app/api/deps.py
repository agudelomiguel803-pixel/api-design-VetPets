# app/api/deps.py
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.repositories import (
    AppointmentRepository,
    PetsRepository,
    TreatmentRepository,
    VeterinariansRepository
)

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_appointment_repository(session: SessionDep) -> AppointmentRepository:
    """Instancia AppointmentRepository con la sesión de BD activa."""
    return AppointmentRepository(session)


def get_pets_repository(session: SessionDep) -> PetsRepository:
    """Instancia PetsRepository con la sesión de BD activa."""
    return PetsRepository(session)


def get_treatment_repository(session: SessionDep) -> TreatmentRepository:
    """Instancia TreatmentRepository con la sesión de BD activa."""
    return TreatmentRepository(session)


def get_veterinarian_repository(session: SessionDep) -> VeterinariansRepository:
    """Instancia VeterinariansRepository con la sesión de BD activa."""
    return VeterinariansRepository(session)