# app/api/routers/veterinarians.py
from fastapi import APIRouter, status

from app.api.deps import VeterinarianServiceDep
from app.models.veterinarians import VeterinarioCreate, VeterinarioPublic, VeterinarioUpdate

router = APIRouter(prefix="/veterinarians", tags=["Veterinarians"])

@router.post(
    "/",
    response_model=VeterinarioPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Crear veterinario",
    description="Registra un nuevo veterinario en el sistema.",
)
async def create_veterinarian(
    veterinario_in: VeterinarioCreate,
    service: VeterinarianServiceDep,
) -> VeterinarioPublic:
    return await service.create(veterinario_in)

@router.get(
    "/",
    response_model=list[VeterinarioPublic],
    summary="Listar veterinarios",
    description="Obtiene una lista paginada de veterinarios.",
)
async def list_veterinarians(
    service: VeterinarianServiceDep,
    skip: int = 0,
    limit: int = 100,
) -> list[VeterinarioPublic]:
    return await service.list_all(skip=skip, limit=limit)

@router.get(
    "/{veterinario_id}",
    response_model=VeterinarioPublic,
    summary="Obtener veterinario por ID",
    description="Busca un veterinario por ID o devuelve 404 Not Found.",
)
async def get_veterinarian(
    veterinario_id: int,
    service: VeterinarianServiceDep,
) -> VeterinarioPublic:
    return await service.get_by_id(veterinario_id)

@router.patch(
    "/{veterinario_id}",
    response_model=VeterinarioPublic,
    summary="Actualizar veterinario",
    description="Actualiza campos específicos de un veterinario existente.",
)
async def update_veterinarian(
    veterinario_id: int,
    veterinario_in: VeterinarioUpdate,
    service: VeterinarianServiceDep,
) -> VeterinarioPublic:
    return await service.update(veterinario_id, veterinario_in)

@router.delete(
    "/{veterinario_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar veterinario",
    description="Elimina un veterinario del sistema.",
)
async def delete_veterinarian(
    veterinario_id: int,
    service: VeterinarianServiceDep,
) -> None:
    await service.delete(veterinario_id)