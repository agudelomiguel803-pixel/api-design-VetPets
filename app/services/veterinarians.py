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
                detail="Este Veterinario no fue encontrado",
            )
        return item

    async def list_all(self, skip: int = 0, limit: int = 100) -> list[Veterinario]:
        return await self.vet_repo.get_multi(skip=skip, limit=limit)

    async def create(self, vet_in: VeterinarioCreate) -> Veterinario:
        existing_licencia = await self.vet_repo.get_by_licencia(vet_in.licencia)
        if existing_licencia:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Hay un veterinario con esa licencia",
            )

        existing_email = await self.vet_repo.get_by_email(vet_in.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Hay un veterinario con ese correo",
            )

        return await self.vet_repo.create(vet_in)

    async def update(self, vet_id: int, vet_in: VeterinarioUpdate) -> Veterinario:
        item = await self.get_by_id(vet_id)

        if vet_in.licencia is not None and vet_in.licencia != item.licencia:
            existing_licencia = await self.vet_repo.get_by_licencia(vet_in.licencia)
            if existing_licencia and existing_licencia.id != vet_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Hay un veterinario con esa licencia",
                )

        if vet_in.email is not None and vet_in.email != item.email:
            existing_email = await self.vet_repo.get_by_email(vet_in.email)
            if existing_email and existing_email.id != vet_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Hay un veterinario con ese correo",
                )

        return await self.vet_repo.update(item, vet_in)

    async def delete(self, vet_id: int) -> None:
        item = await self.get_by_id(vet_id)
        await self.vet_repo.delete(item)