from datetime import datetime, timezone

from sqlmodel import Field, SQLModel
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.cite import Cite


class TreatmentBase(SQLModel):
    """Atributos comunes compartidos por la base de datos y la API."""

    descripcion: str = Field(
        min_length=3,
        max_length=500,
        description="Descripción del tratamiento",
    )
    dosis: str = Field(
        min_length=1,
        max_length=100,
        description="Dosis indicada (por ejemplo, '500 mg cada 8 horas')",
    )
    id_cita: int = Field(
        foreign_key="cita.id",
        index=True,
        description="Identificador de la cita a la que pertenece el tratamiento",
    )


class Treatment(TreatmentBase, table=True):
    """Modelo de tabla: TRATAMIENTO."""

    __tablename__ = "tratamiento"

    id: int | None = Field(
        default=None,
        primary_key=True,
        description="Identificador único del tratamiento",
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
    )
    cita: "Cita | None" = Relationship(back_populates="tratamientos")
   


class TreatmentCreate(TreatmentBase):
    """Schema con los datos requeridos para registrar un nuevo tratamiento."""

    pass


class TreatmentUpdate(SQLModel):
    """Schema para actualizar tratamientos (todos los campos son opcionales)."""

    descripcion: str | None = Field(default=None, min_length=3, max_length=500)
    dosis: str | None = Field(default=None, min_length=1, max_length=100)
    id_cita: int | None = Field(default=None)


class TreatmentPublic(TreatmentBase):
    """Schema público devuelto al cliente por la API."""

    id: int
    created_at: datetime
    updated_at: datetime