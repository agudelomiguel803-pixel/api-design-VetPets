from fastapi import APIRouter, status

from app.api.deps import PetServiceDep
from app.models.pets import PetCreate, PetPublic, PetUpdate

router = APIRouter(prefix="/pets", tags=["Pets"])


@router.post(
    "/",
    response_model=PetPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Crear mascota",
    description="Registra una nueva mascota en el sistema.",
)
async def create_pet(
    pet_in: PetCreate,
    service: PetServiceDep,
) -> PetPublic:
    return await service.create(pet_in)


@router.get(
    "/",
    response_model=list[PetPublic],
    summary="Listar mascotas",
    description="Obtiene una lista paginada de mascotas.",
)
async def list_pets(
    service: PetServiceDep,
    skip: int = 0,
    limit: int = 100,
) -> list[PetPublic]:
    return await service.list_all(skip=skip, limit=limit)


@router.get(
    "/{pet_id}",
    response_model=PetPublic,
    summary="Obtener mascota por ID",
    description="Busca una mascota por ID o devuelve 404 Not Found.",
)
async def get_pet(
    pet_id: int,
    service: PetServiceDep,
) -> PetPublic:
    return await service.get_by_id(pet_id)


@router.patch(
    "/{pet_id}",
    response_model=PetPublic,
    summary="Actualizar mascota",
    description="Actualiza campos específicos de una mascota existente.",
)
async def update_pet(
    pet_id: int,
    pet_in: PetUpdate,
    service: PetServiceDep,
) -> PetPublic:
    return await service.update(pet_id, pet_in)


@router.delete(
    "/{pet_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar mascota",
    description="Elimina una mascota del sistema.",
)
async def delete_pet(
    pet_id: int,
    service: PetServiceDep,
) -> None:
    await service.delete(pet_id)