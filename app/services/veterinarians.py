"""
Capa de Lógica de Negocio (Servicio) para Veterinarios
Ubicación: app/services/veterinarians.py
"""
from fastapi import HTTPException, status
from app.models.veterinarians import Veterinario, VeterinarioCreate, VeterinarioUpdate
from app.repositories.veterinarians import VeterinariansRepository

class VeterinarianService:
    """Capa de Lógica de Negocio para Veterinarios."""

    def __init__(self, vet_repo: VeterinariansRepository) -> None:
        self.vet_repo = vet_repo

    async def get_by_id(self, vet_id: int) -> Veterinario:
        item = await self.vet_repo.get_by_id(vet_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Veterinario no encontrado",
            )
        return item

    async def list_all(self, skip: int = 0, limit: int = 100) -> list[Veterinario]:
        return await self.vet_repo.get_multi(skip=skip, limit=limit)

    async def create(self, vet_in: VeterinarioCreate) -> Veterinario:
        # TODO: Colocar aquí reglas de unicidad o validación previa si se requiere (ej. validar si la licencia ya existe)
        return await self.vet_repo.create(vet_in)

    async def update(self, vet_id: int, vet_in: VeterinarioUpdate) -> Veterinario:
        item = await self.get_by_id(vet_id)
        # TODO: Colocar aquí validaciones previas a la actualización
        return await self.vet_repo.update(item, vet_in)

    async def delete(self, vet_id: int) -> None:
        item = await self.get_by_id(vet_id)
        await self.vet_repo.delete(item)