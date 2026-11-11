"""
Servicio de Citas
Ubicación: app/services/cite.py
"""
from datetime import datetime, timezone

from fastapi import HTTPException, status

from app.models.cite import Appointment, AppointmentCreate, AppointmentUpdate
from app.repositories.cite import AppointmentRepository
from app.repositories.pets import PetsRepository
from app.repositories.veterinarians import VeterinariansRepository


class AppointmentService:
    """
    Capa de Lógica de Negocio para Citas.
    Valida mascota, veterinario y disponibilidad antes de persistir.
    """

    def __init__(
        self,
        appointment_repo: AppointmentRepository,
        pets_repo: PetsRepository,
        veterinarians_repo: VeterinariansRepository,
    ) -> None:
        self.appointment_repo = appointment_repo
        self.pets_repo = pets_repo
        self.veterinarians_repo = veterinarians_repo

    async def get_by_id(self, appointment_id: int) -> Appointment:
        """Busca una cita por ID o lanza 404 si no existe."""
        appointment = await self.appointment_repo.get_by_id(appointment_id)
        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cita no encontrada",
            )
        return appointment

    async def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        id_mascota: int | None = None,
        id_veterinario: int | None = None,
    ) -> list[Appointment]:
        """Obtiene la lista de citas paginada, con filtros opcionales."""
        return await self.appointment_repo.get_multi(
            skip=skip,
            limit=limit,
            id_mascota=id_mascota,
            id_veterinario=id_veterinario,
        )

    async def create(self, appointment_in: AppointmentCreate) -> Appointment:
        """
        Reglas de negocio:
        - La mascota debe existir.
        - El veterinario debe existir.
        - La fecha debe ser futura.
        - El veterinario no puede tener otra cita a la misma hora.
        """
        await self._validate_pet(appointment_in.id_mascota)
        await self._validate_veterinarian(appointment_in.id_veterinario)
        self._validate_future_date(appointment_in.fecha_hora)
        await self._validate_availability(
            appointment_in.id_veterinario, appointment_in.fecha_hora
        )
        return await self.appointment_repo.create(appointment_in)

    async def update(
        self, appointment_id: int, appointment_in: AppointmentUpdate
    ) -> Appointment:
        """
        Reglas de negocio:
        - La cita debe existir.
        - Si cambia la mascota o el veterinario, el nuevo debe existir.
        - Si cambia la fecha, debe ser futura.
        - Si cambia la fecha o el veterinario, no puede haber cruce de horarios.
        """
        appointment = await self.get_by_id(appointment_id)

        new_pet = appointment_in.id_mascota
        new_vet = appointment_in.id_veterinario
        new_date = appointment_in.fecha_hora

        if new_pet is not None and new_pet != appointment.id_mascota:
            await self._validate_pet(new_pet)

        if new_vet is not None and new_vet != appointment.id_veterinario:
            await self._validate_veterinarian(new_vet)

        if new_date is not None and new_date != appointment.fecha_hora:
            self._validate_future_date(new_date)

        vet_changed = new_vet is not None and new_vet != appointment.id_veterinario
        date_changed = new_date is not None and new_date != appointment.fecha_hora
        if vet_changed or date_changed:
            await self._validate_availability(
                new_vet if new_vet is not None else appointment.id_veterinario,
                new_date if new_date is not None else appointment.fecha_hora,
                exclude_id=appointment.id,
            )

        return await self.appointment_repo.update(appointment, appointment_in)

    async def delete(self, appointment_id: int) -> None:
        """Elimina una cita previa verificación de su existencia."""
        appointment = await self.get_by_id(appointment_id)
        await self.appointment_repo.delete(appointment)

    # ------------------------------------------------------------------
    # Validaciones auxiliares (reutilizadas por create y update)
    # ------------------------------------------------------------------
    async def _validate_pet(self, pet_id: int) -> None:
        pet = await self.pets_repo.get_by_id(pet_id)
        if not pet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="La mascota indicada no existe",
            )

    async def _validate_veterinarian(self, veterinarian_id: int) -> None:
        vet = await self.veterinarians_repo.get_by_id(veterinarian_id)
        if not vet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El veterinario indicado no existe",
            )

    @staticmethod
    def _validate_future_date(fecha_hora: datetime) -> None:
        fecha = fecha_hora
        if fecha.tzinfo is None:
            fecha = fecha.replace(tzinfo=timezone.utc)
        if fecha <= datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La fecha y hora de la cita debe ser futura",
            )

    async def _validate_availability(
        self,
        veterinarian_id: int,
        fecha_hora: datetime,
        exclude_id: int | None = None,
    ) -> None:
        existing = await self.appointment_repo.get_by_veterinarian_and_datetime(
            veterinarian_id, fecha_hora, exclude_id=exclude_id
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El veterinario ya tiene una cita en esa fecha y hora",
            )