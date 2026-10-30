from datetime import datetime, timezone
from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.cita import Cita


class VeterinarioBase(SQLModel):
    """Atributos comunes compartidos por la base de datos y la API para Veterinario."""

    nombre: str = Field(
        min_length=2,
        max_length=100,
        description="Nombre completo del veterinario",
    )
    especialidad: str = Field(
        min_length=2,
        max_length=100,
        description="Especialidad médica o área de enfoque",
    )
    licencia: str = Field(
        index=True,
        unique=True,
        description="Número de licencia o tarjeta profesional",
    )
    email: str = Field(
        index=True,
        description="Correo electrónico de contacto del veterinario",
    )


class Veterinario(VeterinarioBase, table=True):
    """Tabla física en la base de datos para almacenar veterinarios."""

    __tablename__ = "veterinarios"

    id: int | None = Field(
        default=None,
        primary_key=True,
        description="Identificador único autoincremental (PK)",
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
        description="Fecha y hora en que se creó el registro",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
        description="Fecha y hora de la última actualización del registro",
    )

    # LADO '1': Un veterinario tiene muchas citas asociadas (Relación 1:N)[cite: 1]
    citas: list["Cita"] = Relationship(back_populates="veterinario")


class VeterinarioCreate(VeterinarioBase):
    """Schema con los datos requeridos para registrar un nuevo veterinario."""
    pass


class VeterinarioUpdate(SQLModel):
    """Schema para actualizar veterinarios (todos los campos son opcionales)."""

    nombre: str | None = Field(default=None, min_length=2, max_length=100)
    especialidad: str | None = Field(default=None, min_length=2, max_length=100)
    licencia: str | None = Field(default=None)
    email: str | None = Field(default=None)


class VeterinarioPublic(VeterinarioBase):
    """Schema público devuelto al cliente por la API."""

    id: int
    created_at: datetime
    updated_at: datetime