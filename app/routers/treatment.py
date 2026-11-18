from fastapi import APIRouter, status


from app.api.deps import TreatmentServiceDep
from app.models.treatment import (
    TreatmentCreate,
    TreatmentUpdate,
    Treatment,
)


router = APIRouter(prefix="/treatments", tags=["Treatments"])




@router.post(
    "/",
    response_model=Treatment,
    status_code=status.HTTP_201_CREATED,
    summary="Crear tratamiento",
    description="Registra un nuevo tratamiento en el sistema.",
)
async def create_treatment(
    treatment_in: TreatmentCreate,
    service: TreatmentServiceDep,
) -> Treatment:
    return await service.create(treatment_in)




@router.get(
    "/",
    response_model=list[Treatment],
    summary="Listar tratamientos",
    description="Obtiene una lista paginada de tratamientos.",
)
async def list_treatments(
    service: TreatmentServiceDep,
    skip: int = 0,
    limit: int = 100,
) -> list[Treatment]:
    return await service.list_all(skip=skip, limit=limit)




@router.get(
    "/{treatment_id}",
    response_model=Treatment,
    summary="Obtener tratamiento por ID",
    description="Busca un tratamiento por ID o devuelve 404 Not Found.",
)
async def get_treatment(
    treatment_id: int,
    service: TreatmentServiceDep,
) -> Treatment:
    return await service.get_by_id(treatment_id)




@router.patch(
    "/{treatment_id}",
    response_model=Treatment,
    summary="Actualizar tratamiento",
    description="Actualiza campos específicos de un tratamiento existente.",
)
async def update_treatment(
    treatment_id: int,
    treatment_in: TreatmentUpdate,
    service: TreatmentServiceDep,
) -> Treatment:
    return await service.update(treatment_id, treatment_in)




@router.delete(
    "/{treatment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar tratamiento",
    description="Elimina un tratamiento del sistema.",
)
async def delete_treatment(
    treatment_id: int,
    service: TreatmentServiceDep,
) -> None:
    await service.delete(treatment_id)