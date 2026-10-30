from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.pets import Pet
    # Descomentar cuando hagas merge de las ramas de tus compañeros
    # y verifiques que el nombre de la clase coincida exactamente:
    # from app.models.veterinarians import Veterinarians
    # from app.models.treatment import Treatment


class CitaBase(SQLModel):
    """Atributos comunes compartidos para la gestión de citas médicas en VetPets"""

    fecha_hora: datetime = Field(
        description="Fecha y hora exacta programada para la cita"
    )
    motivo: str = Field(
        min_length=3,
        max_length=255,
        description="Motivo o razón de la consulta veterinaria",
    )
    estado: str = Field(
        default="pendiente",
        max_length=50,
        description="Estado actual de la cita (ej. pendiente, completada, cancelada)",
    )
    # IMPORTANTE: foreign_key usa el __tablename__ de la otra tabla.
    # Verifica que el modelo de veterinarios tenga __tablename__ = "veterinarians".
    id_veterinario: int = Field(
        foreign_key="veterinarians.id",
        index=True,
        description="Identificador único del veterinario asignado",
    )
    id_mascota: int = Field(
        foreign_key="pets.id",
        index=True,
        description="Identificador único de la mascota paciente",
    )


class Appointment(CitaBase, table=True):
    """Tabla física en la base de datos para almacenar las citas médicas."""

    __tablename__ = "appointments"

    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relación N:1 hacia Mascota (Pet)
    pet: Optional["Pet"] = Relationship(back_populates="appointments")

    # Descomentar cuando existan los modelos de tus compañeros
    # (y que en esos modelos exista el back_populates="appointment" / "veterinarian"):
    #
    # # Relación N:1 hacia Veterinario
    # veterinarian: Optional["Veterinarians"] = Relationship(back_populates="appointments")
    #
    # # Relación 1:N hacia Tratamientos (una cita genera muchos tratamientos)
    # treatments: list["Treatment"] = Relationship(
    #     back_populates="appointment", cascade_delete=True
    # )


class AppointmentCreate(CitaBase):
    """Schema con los datos requeridos para registrar una nueva cita médica."""

    pass


class AppointmentUpdate(SQLModel):
    """Schema para actualizar citas médicas (todos los campos son opcionales)."""

    fecha_hora: datetime | None = Field(
        default=None,
        description="Nueva fecha y hora para la cita",
    )
    motivo: str | None = Field(
        default=None,
        min_length=3,
        max_length=255,
        description="Nuevo motivo de la consulta",
    )
    estado: str | None = Field(
        default=None,
        max_length=50,
        description="Nuevo estado de la cita",
    )
    id_veterinario: int | None = Field(
        default=None,
        description="Nuevo ID del veterinario asignado",
    )
    id_mascota: int | None = Field(
        default=None,
        description="Nuevo ID de la mascota paciente",
    )


class AppointmentPublic(CitaBase):
    """Schema con los datos públicos que la API devuelve al cliente."""

    id: int
    created_at: datetime
    updated_at: datetime