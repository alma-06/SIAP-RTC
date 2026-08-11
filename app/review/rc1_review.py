from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class ReviewFinding:
    code: str
    severity: str
    message: str


@dataclass(frozen=True)
class RC1Review:
    findings: tuple[ReviewFinding, ...]
    input_records: int
    normalized_records: int
    deduplicated_records: int
    consolidated_records: int

    @property
    def blocking(self) -> bool:
        return any(item.severity == "BLOCKING" for item in self.findings)


def review_counts(
    input_records: int,
    normalized_records: int,
    deduplicated_records: int,
    consolidated_records: int,
    findings: Iterable[ReviewFinding] = (),
) -> RC1Review:
    derived = list(findings)
    if normalized_records > input_records:
        derived.append(ReviewFinding("COUNT-001", "BLOCKING", "La normalización aumentó el número de registros."))
    if deduplicated_records > normalized_records:
        derived.append(ReviewFinding("COUNT-002", "BLOCKING", "La deduplicación aumentó el número de registros."))
    if consolidated_records > deduplicated_records:
        derived.append(ReviewFinding("COUNT-003", "BLOCKING", "La consolidación aumentó el número de registros."))
    return RC1Review(tuple(derived), input_records, normalized_records, deduplicated_records, consolidated_records)
