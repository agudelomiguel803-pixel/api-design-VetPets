from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.repositories import (
    AppointmentRepository,
    PetsRepository,
    TreatmentRepository,
    VeterinariansRepository,
)
from app.services.cite import AppointmentService
from app.services.pets import PetService            
from app.services.treatment import TreatmentService
from app.services.veterinarians import VeterinarianService

SessionDep = Annotated[AsyncSession, Depends(get_session)]

# --- Fábricas de Repositorios ---
def get_appointment_repository(session: SessionDep) -> AppointmentRepository:
    return AppointmentRepository(session)

def get_pets_repository(session: SessionDep) -> PetsRepository:
    return PetsRepository(session)

def get_treatment_repository(session: SessionDep) -> TreatmentRepository:
    return TreatmentRepository(session)

def get_veterinarian_repository(session: SessionDep) -> VeterinariansRepository:
    return VeterinariansRepository(session)

# --- Aliases Annotated para Repositorios ---
AppointmentRepoDep = Annotated[AppointmentRepository, Depends(get_appointment_repository)]
PetsRepoDep = Annotated[PetsRepository, Depends(get_pets_repository)]
TreatmentRepoDep = Annotated[TreatmentRepository, Depends(get_treatment_repository)]
VeterinarianRepoDep = Annotated[VeterinariansRepository, Depends(get_veterinarian_repository)]

# --- Fábricas de Servicios ---
def get_appointment_service(
    appointment_repo: AppointmentRepoDep,
    pets_repo: PetsRepoDep,
    veterinarians_repo: VeterinarianRepoDep,
) -> AppointmentService:
    return AppointmentService(
        appointment_repo=appointment_repo,
        pets_repo=pets_repo,
        veterinarians_repo=veterinarians_repo,
    )

def get_pet_service(pets_repo: PetsRepoDep) -> PetService:
    return PetService(pets_repo)

def get_treatment_service(treatment_repo: TreatmentRepoDep) -> TreatmentService:
    return TreatmentService(treatment_repo)

def get_veterinarian_service(veterinarians_repo: VeterinarianRepoDep) -> VeterinarianService:
    return VeterinarianService(veterinarians_repo)

# --- Aliases Annotated requeridos por los Routers ---
AppointmentServiceDep = Annotated[AppointmentService, Depends(get_appointment_service)]
PetServiceDep = Annotated[PetService, Depends(get_pet_service)]
TreatmentServiceDep = Annotated[TreatmentService, Depends(get_treatment_service)]
VeterinarianServiceDep = Annotated[VeterinarianService, Depends(get_veterinarian_service)]