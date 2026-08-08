"""Transactional persistence adapter for canonical RTC imports."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from uuid import UUID

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.domain.entities import ImportBatch, RtcSourceFile
from app.domain.rtc import RtcRecord
from app.domain.value_objects import FileHash
from app.infrastructure.orm import Base, ImportBatchModel, ImportBatchSourceModel, RtcRecordModel, SourceFileModel


class RtcPersistence:
    """Persist one complete import batch atomically."""

    def __init__(self, database_url: str) -> None:
        self.engine = create_engine(database_url, future=True)
        Base.metadata.create_all(self.engine)

    def persist_batch(
        self,
        batch: ImportBatch,
        sources: list[RtcSourceFile],
        records: list[RtcRecord],
    ) -> None:
        """Persist sources, batch and records in one transaction."""
        with Session(self.engine) as session:
            with session.begin():
                for source in sources:
                    existing = session.scalar(
                        select(SourceFileModel).where(SourceFileModel.sha256 == source.sha256.value)
                    )
                    if existing is None:
                        session.add(
                            SourceFileModel(
                                id=str(source.id), path=str(source.path),
                                sha256=source.sha256.value, received_at=source.received_at,
                            )
                        )
                session.add(
                    ImportBatchModel(
                        id=str(batch.id), started_at=batch.started_at,
                        finished_at=batch.finished_at,
                        imported_count=len(records),
                        rejected_count=batch.rejected_count,
                        duplicate_count=batch.duplicate_count,
                    )
                )
                for source in sources:
                    session.add(
                        ImportBatchSourceModel(
                            batch_id=str(batch.id), source_file_id=str(source.id)
                        )
                    )
                for record in records:
                    key = record.business_key.normalized()
                    existing_record = session.scalar(
                        select(RtcRecordModel).where(
                            RtcRecordModel.pauta_transmision == key[0],
                            RtcRecordModel.estado == key[1],
                            RtcRecordModel.tiempo_fiscal == key[2],
                            RtcRecordModel.canal_base == key[3],
                            RtcRecordModel.orden == key[4],
                            RtcRecordModel.fecha == record.fecha,
                            RtcRecordModel.dependencia == key[6],
                            RtcRecordModel.clave == key[7],
                            RtcRecordModel.campana == key[8],
                            RtcRecordModel.version == key[9],
                        )
                    )
                    if existing_record is None:
                        session.add(
                            RtcRecordModel(
                                batch_id=str(batch.id),
                                pauta_transmision=key[0], estado=key[1],
                                tiempo_fiscal=key[2], canal_base=key[3], orden=key[4],
                                fecha=record.fecha, dependencia=key[6], clave=key[7],
                                campana=key[8], version=key[9],
                                source_row_number=record.source_row_number,
                            )
                        )
