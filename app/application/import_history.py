"""Import batch history queries for audit and traceability."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.infrastructure.orm import ImportBatchModel, ImportBatchSourceModel, SourceFileModel


class ImportHistoryService:
    """Read-only access to import execution history."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def list_batches(self, limit: int = 100) -> list[ImportBatchModel]:
        if limit < 1:
            raise ValueError("limit debe ser mayor que cero")
        statement = select(ImportBatchModel).order_by(ImportBatchModel.started_at.desc()).limit(limit)
        return list(self._session.scalars(statement).all())

    def source_files(self, batch_id: str) -> list[SourceFileModel]:
        statement = (
            select(SourceFileModel)
            .join(ImportBatchSourceModel, ImportBatchSourceModel.source_file_id == SourceFileModel.id)
            .where(ImportBatchSourceModel.batch_id == batch_id)
            .order_by(SourceFileModel.path)
        )
        return list(self._session.scalars(statement).all())
