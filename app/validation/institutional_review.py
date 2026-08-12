from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ReviewStatus(str, Enum):
    PENDING = "PENDING"
    OBSERVED = "OBSERVED"
    CONFORMING = "CONFORMING"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class InstitutionalReview:
    technical_complete: bool
    documentary_complete: bool
    integrity_ok: bool
    reconciliation_ok: bool
    criterion78_ok: bool
    findings_resolved: bool
    observations: tuple[str, ...] = ()


def evaluate_review(review: InstitutionalReview) -> ReviewStatus:
    critical = (
        review.technical_complete,
        review.documentary_complete,
        review.integrity_ok,
        review.reconciliation_ok,
        review.criterion78_ok,
        review.findings_resolved,
    )
    if not all(critical):
        return ReviewStatus.BLOCKED
    if review.observations:
        return ReviewStatus.OBSERVED
    return ReviewStatus.CONFORMING
