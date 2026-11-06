# app/repositories/cite.py
from datetime import datetime, timezone
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.cite import Appointment, AppointmentCreate, AppointmentUpdate

class AppointmentRepository:
    """Capa 3 - Acceso a Datos puro para citas."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, appointment_id: int) -> Appointment | None:
        """Busca una cita por su clave primaria (ID)."""
        return await self.session.get(Appointment, appointment_id)
    
    async def get_multi(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        id_mascota: int | None = None,
        id_veterinario: int | None = None,
    ) -> list[Appointment]:
        """Obtiene un listado paginado de citas con filtros opcionales."""
        statement = select(Appointment)

        # Filtro opcional por mascota usando el atributo correcto del modelo
        if id_mascota is not None:
            statement = statement.where(Appointment.id_mascota == id_mascota)

        # Filtro opcional por veterinario usando el atributo correcto del modelo
        if id_veterinario is not None:
            statement = statement.where(
                Appointment.id_veterinario == id_veterinario
            )

        statement = statement.order_by(Appointment.id).offset(skip).limit(limit)
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def create(self, appointment_in: AppointmentCreate) -> Appointment:
        """Inserta una nueva cita en la base de datos."""
        db_appointment = Appointment.model_validate(appointment_in)
        self.session.add(db_appointment)
        await self.session.commit()
        await self.session.refresh(db_appointment)
        return db_appointment

    async def update(
        self, db_appointment: Appointment, appointment_in: AppointmentUpdate
    ) -> Appointment:
        """Actualiza únicamente los campos que el cliente envió."""
        update_data: dict[str, Any] = appointment_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_appointment, field, value)

        db_appointment.updated_at = datetime.now(timezone.utc)
        self.session.add(db_appointment)
        await self.session.commit()
        await self.session.refresh(db_appointment)
        return db_appointment

    async def delete(self, db_appointment: Appointment) -> None:
        """Elimina físicamente una cita de la base de datos."""
        await self.session.delete(db_appointment)
        await self.session.commit()