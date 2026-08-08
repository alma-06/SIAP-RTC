"""Core domain entities for source files and import batches."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from uuid import UUID, uuid4

from app.domain.value_objects import FileHash


@dataclass(slots=True)
class RtcSourceFile:
    """A source file received from the RTC publication process."""

    path: Path
    sha256: FileHash
    received_at: datetime
    id: UUID = field(default_factory=uuid4)


@dataclass(slots=True)
class ImportBatch:
    """A traceable processing execution for one or more source files."""

    source_file_ids: list[UUID]
    started_at: datetime
    id: UUID = field(default_factory=uuid4)
    finished_at: datetime | None = None
    imported_count: int = 0
    rejected_count: int = 0
    duplicate_count: int = 0

    def finish(self, finished_at: datetime) -> None:
        if finished_at < self.started_at:
            raise ValueError("finished_at cannot precede started_at")
        self.finished_at = finished_at
