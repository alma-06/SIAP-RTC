from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4


@dataclass(frozen=True)
class FileImportResult:
    filename: str
    sha256: str
    status: str
    records_read: int = 0
    cam_sen_records: int = 0
    duplicates: int = 0
    rejected: int = 0
    new_records: int = 0
    error: str | None = None


@dataclass
class ImportBatchResult:
    batch_id: str = field(default_factory=lambda: f"RTC-{uuid4().hex[:12].upper()}")
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    files: list[FileImportResult] = field(default_factory=list)
    status: str = "INICIADO"

    @property
    def records_read(self) -> int:
        return sum(item.records_read for item in self.files)

    @property
    def cam_sen_records(self) -> int:
        return sum(item.cam_sen_records for item in self.files)

    @property
    def duplicates(self) -> int:
        return sum(item.duplicates for item in self.files)

    @property
    def rejected(self) -> int:
        return sum(item.rejected for item in self.files)

    @property
    def new_records(self) -> int:
        return sum(item.new_records for item in self.files)

    @property
    def spots_count(self) -> int:
        return self.new_records

    def finish(self, success: bool = True) -> None:
        self.status = "PROCESADO" if success else "ERROR"
