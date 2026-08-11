from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from app.pipeline.rtc_ingest import IngestedRecord


@dataclass(frozen=True)
class ConsolidatedRecord:
    period: str
    source_file: str
    record: IngestedRecord


@dataclass(frozen=True)
class ConsolidationResult:
    records: tuple[ConsolidatedRecord, ...]
    periods: tuple[str, ...]
    source_files: tuple[str, ...]


def consolidate_records(
    records: Iterable[IngestedRecord],
    period: str,
) -> ConsolidationResult:
    consolidated = tuple(
        ConsolidatedRecord(period=period, source_file=record.source_file, record=record)
        for record in records
    )
    source_files = tuple(dict.fromkeys(item.source_file for item in consolidated))
    periods = (period,) if consolidated else ()
    return ConsolidationResult(consolidated, periods, source_files)


def consolidate_history(
    batches: Iterable[tuple[str, Iterable[IngestedRecord]]],
) -> ConsolidationResult:
    records: list[ConsolidatedRecord] = []
    periods: list[str] = []
    source_files: list[str] = []
    for period, batch in batches:
        if period not in periods:
            periods.append(period)
        for record in batch:
            records.append(ConsolidatedRecord(period, record.source_file, record))
            if record.source_file not in source_files:
                source_files.append(record.source_file)
    return ConsolidationResult(tuple(records), tuple(periods), tuple(source_files))
