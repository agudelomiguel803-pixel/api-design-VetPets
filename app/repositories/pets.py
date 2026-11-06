# app/repositories/pets.py
from datetime import datetime, timezone
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.pets import Pet, PetCreate, PetUpdate

class PetsRepository:
    """Capa 3 - Acceso a Datos puro para mascotas."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, pet_id: int) -> Pet | None:
        """Busca una mascota por su clave primaria (ID)."""
        return await self.session.get(Pet, pet_id)

    async def get_multi(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        owner_id: int | None = None,
    ) -> list[Pet]:
        """Obtiene un listado paginado de mascotas con filtros opcionales."""
        statement = select(Pet)

        # Filtro opcional por dueño
        if owner_id is not None:
            statement = statement.where(Pet.owner_id == owner_id)

        statement = statement.order_by(Pet.id).offset(skip).limit(limit)
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def create(self, pet_in: PetCreate) -> Pet:
        """Inserta una nueva mascota en la base de datos."""
        db_pet = Pet.model_validate(pet_in)
        self.session.add(db_pet)
        await self.session.commit()
        await self.session.refresh(db_pet)
        return db_pet

    async def update(self, db_pet: Pet, pet_in: PetUpdate) -> Pet:
        """Actualiza únicamente los campos que el cliente envió."""
        update_data: dict[str, Any] = pet_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_pet, field, value)

        db_pet.updated_at = datetime.now(timezone.utc)
        self.session.add(db_pet)
        await self.session.commit()
        await self.session.refresh(db_pet)
        return db_pet

    async def delete(self, db_pet: Pet) -> None:
        """Elimina físicamente una mascota de la base de datos."""
        await self.session.delete(db_pet)
        await self.session.commit()