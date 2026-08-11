from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from app.pipeline.consolidate import ConsolidatedRecord
from app.pipeline.deduplicate import fingerprint


@dataclass(frozen=True)
class ReconciliationDecision:
    key: str
    classification: str
    previous_source: str | None
    current_source: str | None
    changed_fields: tuple[str, ...]


@dataclass(frozen=True)
class ReconciliationResult:
    decisions: tuple[ReconciliationDecision, ...]
    previous_count: int
    current_count: int
    unchanged_count: int
    added_count: int
    removed_count: int
    modified_count: int


def _identity(record: ConsolidatedRecord) -> str:
    values = record.record.values
    return "|".join(str(values.get(field, "")) for field in (
        "Orden", "Fecha", "Clave", "Campaña", "Versión", "Canal Base"
    ))


def _changed_fields(previous: ConsolidatedRecord, current: ConsolidatedRecord) -> tuple[str, ...]:
    fields = tuple(sorted(set(previous.record.values) | set(current.record.values)))
    return tuple(field for field in fields if previous.record.values.get(field) != current.record.values.get(field))


def reconcile_periods(
    previous: Iterable[ConsolidatedRecord],
    current: Iterable[ConsolidatedRecord],
) -> ReconciliationResult:
    previous_map = {_identity(item): item for item in previous}
    current_map = {_identity(item): item for item in current}
    decisions: list[ReconciliationDecision] = []

    unchanged = added = removed = modified = 0
    for key in sorted(set(previous_map) | set(current_map)):
        old = previous_map.get(key)
        new = current_map.get(key)
        if old is None:
            decisions.append(ReconciliationDecision(key, "added", None, new.source_file, ()))
            added += 1
            continue
        if new is None:
            decisions.append(ReconciliationDecision(key, "removed", old.source_file, None, ()))
            removed += 1
            continue
        changed = _changed_fields(old, new)
        if changed:
            decisions.append(ReconciliationDecision(key, "modified", old.source_file, new.source_file, changed))
            modified += 1
        else:
            decisions.append(ReconciliationDecision(key, "unchanged", old.source_file, new.source_file, ()))
            unchanged += 1

    return ReconciliationResult(
        tuple(decisions), len(previous_map), len(current_map), unchanged, added, removed, modified
    )
