# app/repositories/veterinarians.py
from datetime import datetime, timezone
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.veterinarians import Veterinario, VeterinarioCreate, VeterinarioUpdate

class VeterinariansRepository:
    """Capa 3 - Acceso a Datos (Repositorio) para Veterinarios."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    # 1. READ (Uno)
    async def get_by_id(self, item_id: int) -> Veterinario | None:
        return await self.session.get(Veterinario, item_id)

    # 2. READ (Múltiples)
    async def get_multi(self, *, skip: int = 0, limit: int = 100) -> list[Veterinario]:
        statement = select(Veterinario).order_by(Veterinario.id).offset(skip).limit(limit)
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    # 3. CREATE
    async def create(self, item_in: VeterinarioCreate) -> Veterinario:
        db_item = Veterinario.model_validate(item_in)
        self.session.add(db_item)
        await self.session.commit()
        await self.session.refresh(db_item)
        return db_item

    # 4. UPDATE
    async def update(self, db_item: Veterinario, item_in: VeterinarioUpdate) -> Veterinario:
        update_data: dict[str, Any] = item_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_item, field, value)

        db_item.updated_at = datetime.now(timezone.utc)
        self.session.add(db_item)
        await self.session.commit()
        await self.session.refresh(db_item)
        return db_item

    # 5. DELETE
    async def delete(self, db_item: Veterinario) -> None:
        await self.session.delete(db_item)
        await self.session.commit()
