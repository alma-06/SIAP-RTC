"""Repository contracts owned by the SIAP-RTC domain."""

from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities import ImportBatch, RtcSourceFile


class SourceFileRepository(ABC):
    """Persistence contract for imported RTC source files."""

    @abstractmethod
    def add(self, source_file: RtcSourceFile) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, source_file_id: UUID) -> RtcSourceFile | None:
        raise NotImplementedError


class ImportBatchRepository(ABC):
    """Persistence contract for import processing batches."""

    @abstractmethod
    def add(self, batch: ImportBatch) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, batch_id: UUID) -> ImportBatch | None:
        raise NotImplementedError
