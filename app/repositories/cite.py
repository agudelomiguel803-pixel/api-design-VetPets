# app/repositories/cite.py
from datetime import datetime, timezone
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.cite import Appointment, AppointmentCreate, AppointmentUpdate