"""SQLite database bootstrap for SIAP-RTC."""

from __future__ import annotations

import sqlite3
from pathlib import Path


SCHEMA_VERSION = 1


def initialize_database(database_path: Path) -> None:
    """Create the SQLite database and metadata table if absent."""
    database_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(database_path) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS schema_metadata (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                schema_version INTEGER NOT NULL
            )
            """
        )
        connection.execute(
            "INSERT OR IGNORE INTO schema_metadata (id, schema_version) VALUES (1, ?)",
            (SCHEMA_VERSION,),
        )
        connection.commit()
