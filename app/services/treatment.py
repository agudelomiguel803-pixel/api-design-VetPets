"""
Servicio de Treatment
Ubicación: app/services/treatment.py
"""
from fastapi import HTTPException, status
from app.models.treatment import Treatment, TreatmentCreate, TreatmentUpdate
from app.repositories.treatment import TreatmentRepository


class TreatmentService:
    """Capa de Lógica de Negocio para Treatment."""

    def __init__(self, treatment_repo: TreatmentRepository) -> None:
        self.treatment_repo = treatment_repo

    async def get_by_id(self, treatment_id: int) -> Treatment:
        item = await self.treatment_repo.get_by_id(treatment_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registro no encontrado",
            )
        return item

    async def list_all(self, skip: int = 0, limit: int = 100) -> list[Treatment]:
        return await self.treatment_repo.get_multi(skip=skip, limit=limit)

    async def create(self, treatment_in: TreatmentCreate) -> Treatment:
        # TODO: Colocar aquí reglas de unicidad o validación previa
        return await self.treatment_repo.create(treatment_in)

    async def update(self, treatment_id: int, treatment_in: TreatmentUpdate) -> Treatment:
        item = await self.get_by_id(treatment_id)
        # TODO: Colocar aquí validaciones previas a la actualización
        return await self.treatment_repo.update(item, treatment_in)

    async def delete(self, treatment_id: int) -> None:
        item = await self.get_by_id(treatment_id)
        await self.treatment_repo.delete(item)