from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from app.pipeline.consolidate import ConsolidationResult, consolidate_records
from app.pipeline.deduplicate import DeduplicationResult, deduplicate_records
from app.pipeline.evidence import EvidenceManifest, build_evidence_manifest
from app.pipeline.indicators import IndicatorResult, build_indicators
from app.pipeline.normalize import NormalizationResult, normalize_records
from app.pipeline.reconcile import ReconciliationResult, reconcile_periods
from app.pipeline.rtc_ingest import IngestResult, ingest_rtc_workbooks


@dataclass(frozen=True)
class IntegratedPipelineResult:
    ingestion: IngestResult
    normalization: NormalizationResult
    deduplication: DeduplicationResult
    consolidation: ConsolidationResult
    reconciliation: ReconciliationResult | None
    indicators: IndicatorResult | None
    evidence: EvidenceManifest


def run_integrated_period(
    files: Iterable[str | Path],
    period: str,
    previous: ConsolidationResult | None = None,
    evidence_id: str | None = None,
) -> IntegratedPipelineResult:
    ingestion = ingest_rtc_workbooks(files)
    normalization = normalize_records(ingestion.records)
    deduplication = deduplicate_records(normalization.records)
    consolidation = consolidate_records(deduplication.records, period)

    reconciliation = None
    indicators = None
    if previous is not None:
        reconciliation = reconcile_periods(previous.records, consolidation.records)
        indicators = build_indicators(reconciliation)

    warnings = (*ingestion.warnings, *normalization.warnings)
    evidence = build_evidence_manifest(
        evidence_id or f"EV-{period}",
        "registros de pauta RTC",
        "ingesta, filtrado CAM. SEN., normalización, deduplicación exacta y consolidación",
        ((path, period) for path in files),
        (*warnings, "La pauta RTC no acredita por sí misma transmisión efectiva."),
    )
    return IntegratedPipelineResult(
        ingestion, normalization, deduplication, consolidation,
        reconciliation, indicators, evidence,
    )
