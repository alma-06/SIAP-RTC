from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ReleaseStatus(str, Enum):
    BLOCKED = "BLOCKED"
    RELEASE_CANDIDATE = "RELEASE_CANDIDATE"
    RELEASED = "RELEASED"


@dataclass(frozen=True)
class ReleaseInputs:
    version: str
    commit: str
    run_id: str
    master_record: str
    manifest_verified: bool
    technical_opinion: str
    institutional_review: str
    scope: str


def evaluate_release(inputs: ReleaseInputs) -> ReleaseStatus:
    required = (
        bool(inputs.version),
        bool(inputs.commit),
        bool(inputs.run_id),
        bool(inputs.master_record),
        inputs.manifest_verified,
        inputs.technical_opinion in {"VALIDADO", "VALIDADO_CON_OBSERVACIONES"},
        inputs.institutional_review == "CONFORMING",
        bool(inputs.scope),
    )
    if not all(required):
        return ReleaseStatus.BLOCKED
    return ReleaseStatus.RELEASED
