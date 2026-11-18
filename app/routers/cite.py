from fastapi import APIRouter, status

from app.api.deps import AppointmentServiceDep
from app.models.cite import AppointmentCreate, AppointmentPublic, AppointmentUpdate

router = APIRouter(prefix="/appointments", tags=["Appointments"])

@router.post(
    "/",
    response_model=AppointmentPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Crear cita",
    description="Registra una nueva cita médica aplicando las validaciones de negocio.",
)
async def create_appointment(
    appointment_in: AppointmentCreate,
    service: AppointmentServiceDep,
) -> AppointmentPublic:
    return await service.create(appointment_in)

@router.get(
    "/",
    response_model=list[AppointmentPublic],
    summary="Listar citas",
    description="Obtiene una lista paginada de citas con filtros opcionales.",
)
async def list_appointments(
    service: AppointmentServiceDep,
    skip: int = 0,
    limit: int = 100,
    id_mascota: int | None = None,
    id_veterinario: int | None = None,
) -> list[AppointmentPublic]:
    return await service.list_all(
        skip=skip,
        limit=limit,
        id_mascota=id_mascota,
        id_veterinario=id_veterinario,
    )

@router.get(
    "/{appointment_id}",
    response_model=AppointmentPublic,
    summary="Obtener cita por ID",
    description="Busca una cita específica por ID o devuelve 404 si no existe.",
)
async def get_appointment(
    appointment_id: int,
    service: AppointmentServiceDep,
) -> AppointmentPublic:
    return await service.get_by_id(appointment_id)

@router.patch(
    "/{appointment_id}",
    response_model=AppointmentPublic,
    summary="Actualizar cita",
    description="Actualiza parcialmente una cita existente y valida cruces de horarios.",
)
async def update_appointment(
    appointment_id: int,
    appointment_in: AppointmentUpdate,
    service: AppointmentServiceDep,
) -> AppointmentPublic:
    return await service.update(appointment_id, appointment_in)

@router.delete(
    "/{appointment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar cita",
    description="Elimina una cita del sistema de forma permanente.",
)
async def delete_appointment(
    appointment_id: int,
    service: AppointmentServiceDep,
) -> None:
    await service.delete(appointment_id)