from datetime import date, datetime, timezone
from typing import TYPE_CHECKING, List

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.citas import Cita


class PetBase(SQLModel):
    """Atributos comunes compartidos por la base de datos y la API."""

    nombre: str = Field(
        min_length=2,
        max_length=100,
        index=True,
        description="Nombre de la mascota",
    )
    especie: str = Field(
        max_length=50,
        description="Especie de la mascota (perro, gato, etc.)",
    )
    raza: str = Field(
        max_length=50,
        description="Raza de la mascota",
    )
    fecha_nacimiento: date = Field(
        description="Fecha de nacimiento de la mascota",
    )
    nombre_dueno: str = Field(
        max_length=100,
        description="Nombre del dueño de la mascota",
    )
    telefono_dueno: str = Field(
        max_length=20,
        description="Teléfono de contacto del dueño",
    )


class Pet(PetBase, table=True):
    """Tabla física en la base de datos para almacenar mascotas."""

    __tablename__ = "pets"

    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # LADO 'UNO': una lista de objetos Cita de retorno
    # citas: List["Cita"] = Relationship(back_populates="mascota")


class PetCreate(PetBase):
    """Schema con los datos requeridos para registrar una nueva mascota."""

    pass


class PetUpdate(SQLModel):
    """Schema para actualizar mascotas (todos los campos son opcionales)."""

    nombre: str | None = Field(default=None, min_length=2, max_length=100)
    especie: str | None = Field(default=None, max_length=50)
    raza: str | None = Field(default=None, max_length=50)
    fecha_nacimiento: date | None = Field(default=None)
    nombre_dueno: str | None = Field(default=None, max_length=100)
    telefono_dueno: str | None = Field(default=None, max_length=20)


class PetPublic(PetBase):
    """Schema público devuelto al cliente por la API."""

    id: int
    created_at: datetime
    updated_at: datetime