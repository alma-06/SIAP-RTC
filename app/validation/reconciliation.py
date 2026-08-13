from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ReconciliationStatus(str, Enum):
    MATCHED = "MATCHED"
    PAUTA_ONLY = "PAUTA_ONLY"
    INFRASTRUCTURE_ONLY = "INFRASTRUCTURE_ONLY"
    OBSERVED = "OBSERVED"


@dataclass(frozen=True)
class ReconciliationRecord:
    medium: str
    identifier: str
    infrastructure_present: bool
    commercial: bool
    pauta_present: bool
    cam_sen_spots: int
    status: ReconciliationStatus
    observation: str = ""


def classify(
    *,
    medium: str,
    identifier: str,
    infrastructure_present: bool,
    commercial: bool,
    pauta_present: bool,
    cam_sen_spots: int,
    observation: str = "",
) -> ReconciliationRecord:
    if observation:
        status = ReconciliationStatus.OBSERVED
    elif infrastructure_present and commercial and pauta_present:
        status = ReconciliationStatus.MATCHED
    elif pauta_present and not (infrastructure_present and commercial):
        status = ReconciliationStatus.PAUTA_ONLY
    else:
        status = ReconciliationStatus.INFRASTRUCTURE_ONLY
    return ReconciliationRecord(
        medium=medium,
        identifier=identifier,
        infrastructure_present=infrastructure_present,
        commercial=commercial,
        pauta_present=pauta_present,
        cam_sen_spots=cam_sen_spots,
        status=status,
        observation=observation,
    )
