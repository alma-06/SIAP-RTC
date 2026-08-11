from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path

from app.pipeline.integrated import IntegratedPipelineResult


def build_executive_summary(result: IntegratedPipelineResult) -> dict[str, object]:
    summary: dict[str, object] = {
        "evidence_id": result.evidence.evidence_id,
        "periods": list(result.consolidation.periods),
        "source_files": list(result.consolidation.source_files),
        "records_ingested": len(result.ingestion.records),
        "records_normalized": len(result.normalization.records),
        "records_kept": len(result.deduplication.records),
        "duplicates_removed": sum(
            decision.action == "drop" for decision in result.deduplication.decisions
        ),
        "warnings": list(result.evidence.warnings),
    }
    if result.indicators is not None:
        summary["indicators"] = asdict(result.indicators)
    return summary


def write_executive_summary(result: IntegratedPipelineResult, path: str | Path) -> None:
    payload = build_executive_summary(result)
    Path(path).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
