from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class ReconciliationStatus(str, Enum):
    NEW = "NEW"
    EXISTING = "EXISTING"


@dataclass(frozen=True)
class ReconciliationItem:
    identity_hash: str
    status: ReconciliationStatus


@dataclass(frozen=True)
class ReconciliationSummary:
    source_count: int
    new_count: int
    existing_count: int
    duplicate_source_count: int


def reconcile_identities(source_hashes: Iterable[str], historical_hashes: set[str]) -> tuple[list[ReconciliationItem], ReconciliationSummary]:
    """Compare canonical identities in one source against the historical set.

    Repeated identities inside the incoming source are classified as existing
    after their first occurrence and counted separately as source duplicates.
    The function never mutates the historical set.
    """
    seen: set[str] = set()
    items: list[ReconciliationItem] = []
    duplicate_source_count = 0

    for identity in source_hashes:
        if identity in seen:
            duplicate_source_count += 1
            items.append(ReconciliationItem(identity, ReconciliationStatus.EXISTING))
            continue
        seen.add(identity)
        status = ReconciliationStatus.EXISTING if identity in historical_hashes else ReconciliationStatus.NEW
        items.append(ReconciliationItem(identity, status))

    new_count = sum(item.status is ReconciliationStatus.NEW for item in items)
    existing_count = sum(item.status is ReconciliationStatus.EXISTING for item in items)
    return items, ReconciliationSummary(len(items), new_count, existing_count, duplicate_source_count)
