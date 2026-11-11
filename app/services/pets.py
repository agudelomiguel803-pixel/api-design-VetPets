"""
Servicio para la entidad Pet
Ubicación: app/services/pets.py
"""
from fastapi import HTTPException, status
from app.models.pets import Pet, PetCreate, PetUpdate
from app.repositories.pets import PetsRepository


class PetService:
    """Capa de Lógica de Negocio para Pet."""

    def __init__(self, pet_repo: PetsRepository) -> None:
        self.pet_repo = pet_repo

    async def get_by_id(self, pet_id: int) -> Pet:
        pet = await self.pet_repo.get_by_id(pet_id)
        if not pet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mascota no encontrada",
            )
        return pet

    async def list_all(self, skip: int = 0, limit: int = 100) -> list[Pet]:
        return await self.pet_repo.get_multi(skip=skip, limit=limit)

    async def create(self, pet_in: PetCreate) -> Pet:
        # TODO: reglas previas (ej. validar que el dueño exista)
        return await self.pet_repo.create(pet_in)

    async def update(self, pet_id: int, pet_in: PetUpdate) -> Pet:
        pet = await self.get_by_id(pet_id)
        # TODO: validaciones previas a actualizar
        return await self.pet_repo.update(pet, pet_in)

    async def delete(self, pet_id: int) -> None:
        pet = await self.get_by_id(pet_id)
        await self.pet_repo.delete(pet)