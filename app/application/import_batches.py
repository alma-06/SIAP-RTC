"""Application service for creating and completing import batches."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from app.domain.entities import ImportBatch
from app.domain.repositories import ImportBatchRepository


class ImportBatchService:
    """Coordinate import-batch lifecycle without depending on persistence technology."""

    def __init__(self, repository: ImportBatchRepository) -> None:
        self._repository = repository

    def start(self, source_file_ids: list[UUID], started_at: datetime) -> ImportBatch:
        batch = ImportBatch(source_file_ids=source_file_ids, started_at=started_at)
        self._repository.add(batch)
        return batch

    def finish(self, batch: ImportBatch, finished_at: datetime) -> None:
        batch.finish(finished_at)
        self._repository.add(batch)
