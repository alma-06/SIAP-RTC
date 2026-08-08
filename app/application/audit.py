"""Audit detail queries for SIAP-RTC import batches."""

from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.infrastructure.orm import ImportBatchModel, ImportBatchSourceModel, SourceFileModel, RtcRecordModel


@dataclass(frozen=True, slots=True)
class BatchAuditDetail:
    batch_id: str
    started_at: object
    finished_at: object | None
    imported_count: int
    rejected_count: int
    duplicate_count: int
    source_files: tuple[str, ...]
    source_hashes: tuple[str, ...]
    persisted_records: int


class ImportAuditService:
    """Build a complete audit view for one import batch."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def detail(self, batch_id: str) -> BatchAuditDetail:
        batch = self._session.get(ImportBatchModel, batch_id)
        if batch is None:
            raise ValueError(f"Lote no encontrado: {batch_id}")
        sources = list(self._session.scalars(
            select(SourceFileModel)
            .join(ImportBatchSourceModel, ImportBatchSourceModel.source_file_id == SourceFileModel.id)
            .where(ImportBatchSourceModel.batch_id == batch_id)
            .order_by(SourceFileModel.path)
        ).all())
        persisted = self._session.scalar(
            select(func.count(RtcRecordModel.id)).where(RtcRecordModel.batch_id == batch_id)
        ) or 0
        return BatchAuditDetail(
            batch_id=batch.id,
            started_at=batch.started_at,
            finished_at=batch.finished_at,
            imported_count=batch.imported_count,
            rejected_count=batch.rejected_count,
            duplicate_count=batch.duplicate_count,
            source_files=tuple(s.path for s in sources),
            source_hashes=tuple(s.sha256 for s in sources),
            persisted_records=int(persisted),
        )
