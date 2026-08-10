from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping


class TemporalStatus(str, Enum):
    ADDITION = "ADDITION"
    REMOVAL = "REMOVAL"
    PERSISTENCE = "PERSISTENCE"
    MODIFICATION = "MODIFICATION"


@dataclass(frozen=True)
class TemporalChange:
    identity_hash: str
    status: TemporalStatus
    differences: tuple[str, ...] = ()


def reconcile_periods(
    previous: Mapping[str, Mapping[str, object]],
    current: Mapping[str, Mapping[str, object]],
    comparable_fields: tuple[str, ...],
) -> tuple[TemporalChange, ...]:
    changes: list[TemporalChange] = []
    identities = set(previous) | set(current)
    for identity in sorted(identities):
        if identity not in previous:
            changes.append(TemporalChange(identity, TemporalStatus.ADDITION))
            continue
        if identity not in current:
            changes.append(TemporalChange(identity, TemporalStatus.REMOVAL))
            continue
        differences = tuple(
            field for field in comparable_fields
            if previous[identity].get(field) != current[identity].get(field)
        )
        status = TemporalStatus.MODIFICATION if differences else TemporalStatus.PERSISTENCE
        changes.append(TemporalChange(identity, status, differences))
    return tuple(changes)
