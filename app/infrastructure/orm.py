"""Normalized SQLAlchemy persistence model for SIAP-RTC."""

from __future__ import annotations

from datetime import date, datetime
from uuid import uuid4

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all persistence mappings."""


class SchemaMetadataModel(Base):
    __tablename__ = "schema_metadata"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    schema_version: Mapped[int] = mapped_column(Integer, nullable=False)


class SourceFileModel(Base):
    __tablename__ = "source_file"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    path: Mapped[str] = mapped_column(String(1000), nullable=False)
    sha256: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)
    received_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    import_batches: Mapped[list["ImportBatchSourceModel"]] = relationship(back_populates="source_file")


class ImportBatchModel(Base):
    __tablename__ = "import_batch"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    started_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    imported_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    rejected_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    duplicate_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    source_files: Mapped[list["ImportBatchSourceModel"]] = relationship(back_populates="batch")


class ImportBatchSourceModel(Base):
    __tablename__ = "import_batch_source"
    batch_id: Mapped[str] = mapped_column(ForeignKey("import_batch.id", ondelete="CASCADE"), primary_key=True)
    source_file_id: Mapped[str] = mapped_column(ForeignKey("source_file.id", ondelete="RESTRICT"), primary_key=True)
    batch: Mapped[ImportBatchModel] = relationship(back_populates="source_files")
    source_file: Mapped[SourceFileModel] = relationship(back_populates="import_batches")


class RtcRecordModel(Base):
    __tablename__ = "rtc_record"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    batch_id: Mapped[str] = mapped_column(ForeignKey("import_batch.id", ondelete="RESTRICT"), nullable=False, index=True)
    pauta_transmision: Mapped[str] = mapped_column(String(500), nullable=False)
    estado: Mapped[str] = mapped_column(String(200), nullable=False)
    tiempo_fiscal: Mapped[str] = mapped_column(String(100), nullable=False)
    canal_base: Mapped[str] = mapped_column(String(300), nullable=False)
    orden: Mapped[str] = mapped_column(String(200), nullable=False)
    fecha: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    dependencia: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    clave: Mapped[str] = mapped_column(String(200), nullable=False)
    campana: Mapped[str] = mapped_column(String(500), nullable=False)
    version: Mapped[str] = mapped_column(String(500), nullable=False)
    source_row_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    __table_args__ = (
        UniqueConstraint(
            "pauta_transmision", "estado", "tiempo_fiscal", "canal_base", "orden",
            "fecha", "dependencia", "clave", "campana", "version",
            name="uq_rtc_business_record",
        ),
    )
