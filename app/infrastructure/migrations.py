"""Database schema initialization for the SIAP-RTC persistence layer."""

from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from app.infrastructure.orm import Base

SCHEMA_VERSION = 1


def create_schema(database_url: str) -> Engine:
    """Create the normalized schema and return the configured engine."""
    engine = create_engine(database_url, future=True)
    Base.metadata.create_all(engine)
    return engine
