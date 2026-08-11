from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Iterable

from app.pipeline.rtc_ingest import IngestedRecord, REQUIRED_COLUMNS


@dataclass(frozen=True)
class DuplicateDecision:
    source_file: str
    record_fingerprint: str
    action: str
    reason: str


@dataclass(frozen=True)
class DeduplicationResult:
    records: tuple[IngestedRecord, ...]
    decisions: tuple[DuplicateDecision, ...]


def fingerprint(record: IngestedRecord) -> str:
    canonical = "|".join(str(record.values.get(column, "")) for column in REQUIRED_COLUMNS)
    return sha256(canonical.encode("utf-8")).hexdigest()


def deduplicate_records(records: Iterable[IngestedRecord]) -> DeduplicationResult:
    seen: dict[str, str] = {}
    kept: list[IngestedRecord] = []
    decisions: list[DuplicateDecision] = []

    for record in records:
        key = fingerprint(record)
        if key not in seen:
            seen[key] = record.source_file
            kept.append(record)
            decisions.append(DuplicateDecision(record.source_file, key, "keep", "primer registro con huella única"))
            continue

        original_source = seen[key]
        decisions.append(
            DuplicateDecision(
                record.source_file,
                key,
                "drop",
                f"duplicado exacto del registro proveniente de {original_source}",
            )
        )

    return DeduplicationResult(tuple(kept), tuple(decisions))
