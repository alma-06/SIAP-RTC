from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Iterable
from uuid import uuid4

from app.pipeline.integrated import IntegratedPipelineResult, run_integrated_period
from app.pipeline.evidence import write_evidence_manifest


@dataclass(frozen=True)
class ControlledRun:
    run_id: str
    version: str
    period: str
    output_dir: Path
    result: IntegratedPipelineResult


def execute_controlled_rc1(
    files: Iterable[str | Path],
    period: str,
    output_root: str | Path,
    version: str = "SIAP-RTC v0.1.0-rc1",
) -> ControlledRun:
    run_id = f"RC1-{period}-{uuid4().hex[:8]}"
    output_dir = Path(output_root) / run_id
    output_dir.mkdir(parents=True, exist_ok=False)

    source_files = tuple(Path(path) for path in files)
    result = run_integrated_period(source_files, period, evidence_id=f"{run_id}-EV")

    write_evidence_manifest(result.evidence, output_dir / "EvidenceManifest.json")
    metadata = {
        "run_id": run_id,
        "version": version,
        "period": period,
        "source_files": [str(path) for path in source_files],
        "status": "completed",
    }
    (output_dir / "RunMetadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return ControlledRun(run_id, version, period, output_dir, result)
