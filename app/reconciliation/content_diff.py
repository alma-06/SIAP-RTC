from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping


class ContentStatus(str, Enum):
    IDENTICAL = "IDENTICAL"
    CHANGED = "CHANGED"


@dataclass(frozen=True)
class FieldDifference:
    field: str
    previous: object
    current: object


@dataclass(frozen=True)
class ContentComparison:
    identity_hash: str
    status: ContentStatus
    differences: tuple[FieldDifference, ...]


def compare_content(
    identity_hash: str,
    previous: Mapping[str, object],
    current: Mapping[str, object],
    comparable_fields: tuple[str, ...],
) -> ContentComparison:
    """Compare non-identity fields for a record with the same canonical identity."""
    differences = tuple(
        FieldDifference(field, previous.get(field), current.get(field))
        for field in comparable_fields
        if previous.get(field) != current.get(field)
    )
    status = ContentStatus.CHANGED if differences else ContentStatus.IDENTICAL
    return ContentComparison(identity_hash, status, differences)
