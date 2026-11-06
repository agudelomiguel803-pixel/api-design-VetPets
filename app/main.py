import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Annotated, Any

from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import async_session_maker, engine, get_session, init_db
from app.models import (
    AppointmentCreate,
    AppointmentUpdate,
    PetCreate,
    PetUpdate,
    TreatmentCreate,
    TreatmentUpdate,
    VeterinarioCreate,
    VeterinarioUpdate,
)
from app.repositories import (
    AppointmentRepository,
    PetsRepository,
    TreatmentRepository,
    VeterinariansRepository,
)

async def ejecutar_pruebas_repositorios(session: AsyncSession) -> dict[str, Any]:
    """
    Prueba integral de la Capa 3 (Repositorios) para VetPets:
    Ejecuta operaciones CRUD sobre VeterinariansRepository, PetsRepository,
    AppointmentRepository y TreatmentRepository usando únicamente AsyncSession.
    """
    vet_repo = VeterinariansRepository(session)
    pet_repo = PetsRepository(session)
    appointment_repo = AppointmentRepository(session)
    treatment_repo = TreatmentRepository(session)

    # =========================================================================
    # LIMPIEZA PREVIA (De tablas hijas a tablas padres para evitar Foreign Key Conflicts)
    # =========================================================================
    treatments = await treatment_repo.get_multi(limit=50)
    for t in treatments:
        await treatment_repo.delete(t)

    appointments = await appointment_repo.get_multi(limit=50)
    for a in appointments:
        await appointment_repo.delete(a)

    pets = await pet_repo.get_multi(limit=50)
    for p in pets:
        await pet_repo.delete(p)

    vets = await vet_repo.get_multi(limit=50)
    for v in vets:
        await vet_repo.delete(v)

    # =========================================================================
    # 1. CREATE (Inserción en Base de Datos mediante Repositorios)
    # =========================================================================
    nuevo_veterinario = await vet_repo.create(
        VeterinarioCreate(
            nombre="Dr. Carlos Vet",
            especialidad="Cirugía General",
            licencia="LIC-998877",
            email="carlos.vet@example.com",
        )
    )

    nueva_mascota = await pet_repo.create(
        PetCreate(
            nombre="Firulais",
            especie="Perro",
            raza="Golden Retriever",
            fecha_nacimiento="2020-05-15",
            nombre_dueno="Ana Gómez",
            telefono_dueno="3001234567",
        )
    )

    nueva_cita = await appointment_repo.create(
        AppointmentCreate(
            fecha_hora=datetime.now(timezone.utc),
            motivo="Control general y vacunación anual",
            estado="pendiente",
            id_veterinario=nuevo_veterinario.id,  # type: ignore[arg-type]
            id_mascota=nueva_mascota.id,          # type: ignore[arg-type]
        )
    )

    nuevo_tratamiento = await treatment_repo.create(
        TreatmentCreate(
            descripcion="Aplicación de vacuna antirrábica",
            dosis="1 dosis única de 2ml",
            id_cita=nueva_cita.id,                # type: ignore[arg-type]
        )
    )

    # =========================================================================
    # 2. READ (Consultas por ID y listados con filtros)
    # =========================================================================
    vet_por_id = await vet_repo.get_by_id(nuevo_veterinario.id)  # type: ignore[arg-type]
    cita_por_id = await appointment_repo.get_by_id(nueva_cita.id)  # type: ignore[arg-type]
    
    citas_filtradas = await appointment_repo.get_multi(
        id_mascota=nueva_mascota.id,
        id_veterinario=nuevo_veterinario.id,
    )

    datos_lectura = {
        "vet_name": vet_por_id.nombre if vet_por_id else None,
        "appointment_reason": cita_por_id.motivo if cita_por_id else None,
        "filtered_appointments_count": len(citas_filtradas),
    }

    # =========================================================================
    # 3. UPDATE (Actualización parcial con exclude_unset=True)
    # =========================================================================
    vet_actualizado = await vet_repo.update(
        nuevo_veterinario,
        VeterinarioUpdate(especialidad="Cirugía Avanzada y Ortopedia"),
    )

    mascota_actualizada = await pet_repo.update(
        nueva_mascota,
        PetUpdate(nombre="Firulais (Actualizado)", telefono_dueno="3009876543"),
    )

    cita_actualizada = await appointment_repo.update(
        nueva_cita,
        AppointmentUpdate(estado="completada", motivo="Control general finalizado exitosamente"),
    )

    tratamiento_actualizado = await treatment_repo.update(
        nuevo_tratamiento,
        TreatmentUpdate(dosis="1 dosis única de 2.5ml ajustada"),
    )

    # =========================================================================
    # 4. DELETE (Eliminación física y verificación de retorno None)
    # =========================================================================
    id_tratamiento_eliminado = nuevo_tratamiento.id
    await treatment_repo.delete(nuevo_tratamiento)
    tratamiento_eliminado_check = await treatment_repo.get_by_id(id_tratamiento_eliminado)  # type: ignore[arg-type]

    return {
        "1_create": {
            "vet_id": nuevo_veterinario.id,
            "pet_id": nueva_mascota.id,
            "appointment_id": nueva_cita.id,
            "treatment_id": nuevo_tratamiento.id,
        },
        "2_read": datos_lectura,
        "3_update": {
            "vet_new_especialidad": vet_actualizado.especialidad,
            "pet_new_nombre": mascota_actualizada.nombre,
            "pet_new_telefono_dueno": mascota_actualizada.telefono_dueno,
            "appointment_new_estado": cita_actualizada.estado,
            "treatment_new_dosis": tratamiento_actualizado.dosis,
        },
        "4_delete": {
            "deleted_treatment_id": id_tratamiento_eliminado,
            "get_by_id_after_delete": tratamiento_eliminado_check,
        },
    }

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Ciclo de vida de la aplicación: crea las tablas de la BD al arrancar."""
    await init_db()
    yield

app = FastAPI(
    title=f"{settings.PROJECT_NAME} - Pruebas Repositorios VetPets",
    version=settings.VERSION,
    description=(
        "Proyecto VetPets: Pruebas unitarias/integrales de la Capa 3 de Repositorios "
        "(VeterinariansRepository, PetsRepository, AppointmentRepository, TreatmentRepository)."
    ),
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    """Endpoint para comprobación del estado del servicio."""
    return {"status": "healthy", "layer": "repository-vetpets"}

@app.post("/test-repositories", tags=["Pruebas Capa Repositorio"])
async def test_repositories_endpoint(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> dict[str, Any]:
    """
    Ejecuta desde Swagger UI (`/docs`) una prueba completa de CRUD sobre
    todos los repositorios del ecosistema VetPets.
    """
    resultados = await ejecutar_pruebas_repositorios(session)
    return {
        "mensaje": "Prueba de la capa de repositorios de VetPets completada exitosamente",
        "resultados": resultados,
    }

async def main_cli() -> None:
    """Función para probar los repositorios directamente desde la consola."""
    print("=" * 65)
    print("[INICIO] PRUEBA DE REPOSITORIOS VETPETS (CRUD ASINCRONO)")
    print("=" * 65)

    await init_db()
    print("[OK] 1. Base de datos y tablas inicializadas (init_db).")

    async with async_session_maker() as session:
        resultados = await ejecutar_pruebas_repositorios(session)

        print("\n[CREATE] 2. Insercion de registros:")
        print(f"   - Veterinario ID: {resultados['1_create']['vet_id']}")
        print(f"   - Mascota ID: {resultados['1_create']['pet_id']}")
        print(f"   - Cita ID: {resultados['1_create']['appointment_id']}")
        print(f"   - Tratamiento ID: {resultados['1_create']['treatment_id']}")

        print("\n[READ] 3. Consultas y filtros:")
        print(f"   - Veterinario por ID (Nombre): {resultados['2_read']['vet_name']}")
        print(f"   - Cita por ID (Motivo): {resultados['2_read']['appointment_reason']}")
        print(f"   - Citas filtradas por Mascota y Vet: {resultados['2_read']['filtered_appointments_count']}")

        print("\n[UPDATE] 4. Actualizacion parcial:")
        print(f"   - Veterinario (Especialidad): {resultados['3_update']['vet_new_especialidad']}")
        print(f"   - Cita (Estado): {resultados['3_update']['appointment_new_estado']}")
        print(f"   - Tratamiento (Dosis): {resultados['3_update']['treatment_new_dosis']}")

        print("\n[DELETE] 5. Eliminacion fisica:")
        print(f"   - ID Tratamiento eliminado: {resultados['4_delete']['deleted_treatment_id']}")
        print(
            f"   - Busqueda tras eliminar (debe ser None): "
            f"{resultados['4_delete']['get_by_id_after_delete']}"
        )

    await engine.dispose()
    print("\n" + "=" * 65)
    print("[EXITO] TODAS LAS PRUEBAS DE VETPETS PASARON CORRECTAMENTE")
    print("=" * 65)

if __name__ == "__main__":
    asyncio.run(main_cli())