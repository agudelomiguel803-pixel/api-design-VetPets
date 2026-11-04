# app/repositories/veterinarians.py
from datetime import datetime, timezone
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.veterinarians import Veterinario, VeterinarioCreate, VeterinarioUpdate