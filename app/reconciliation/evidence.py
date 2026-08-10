from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Iterable

from app.reconciliation.comparability import ComparabilityResult
from app.reconciliation.summary import ReconciliationSummary


@dataclass(frozen=True)
class ReconciliationEvidence:
    evidence_id: str
    period: str
    source_file: str
    source_hash: str
    universe_id: str
    methodology_id: str
    record_count: int
    summary: ReconciliationSummary
    comparable: bool
    warnings: tuple[str, ...]
    generated_at: str


def hash_file(path: str | Path) -> str:
    digest = sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_evidence_id(period: str, source_hash: str) -> str:
    return sha256(f"{period}:{source_hash}".encode("utf-8")).hexdigest()[:16]


def build_reconciliation_evidence(
    period: str,
    source_file: str,
    source_hash: str,
    universe_id: str,
    methodology_id: str,
    record_count: int,
    summary: ReconciliationSummary,
    comparability: ComparabilityResult,
    generated_at: str,
    additional_warnings: Iterable[str] = (),
) -> ReconciliationEvidence:
    warnings = tuple(additional_warnings) + comparability.reasons
    return ReconciliationEvidence(
        evidence_id=build_evidence_id(period, source_hash),
        period=period,
        source_file=source_file,
        source_hash=source_hash,
        universe_id=universe_id,
        methodology_id=methodology_id,
        record_count=record_count,
        summary=summary,
        comparable=comparability.comparable,
        warnings=warnings,
        generated_at=generated_at,
    )
