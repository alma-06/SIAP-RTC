"""Application orchestration for end-to-end RTC import."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from app.application.rtc_import import ImportResult, RtcImportPipeline
from app.domain.entities import ImportBatch, RtcSourceFile
from app.domain.value_objects import FileHash
from app.infrastructure.rtc_persistence import RtcPersistence


class RtcImportService:
    """Execute RTC import, build traceable metadata and persist accepted records."""

    def __init__(self, pipeline: RtcImportPipeline, persistence: RtcPersistence) -> None:
        self._pipeline = pipeline
        self._persistence = persistence

    def execute(self, files: list[Path]) -> ImportResult:
        result = self._pipeline.run(files)
        now = datetime.now(timezone.utc)
        sources = [
            RtcSourceFile(
                path=path,
                sha256=FileHash(file_hash),
                received_at=now,
            )
            for path, file_hash in result.file_hashes.items()
        ]
        batch = ImportBatch(
            source_file_ids=[source.id for source in sources],
            started_at=now,
            imported_count=len(result.accepted),
            rejected_count=result.rejected,
            duplicate_count=result.duplicates,
        )
        batch.finish(datetime.now(timezone.utc))
        self._persistence.persist_batch(batch, sources, result.accepted)
        return result
