from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable

from app.dashboard.fact_sheet import ExecutiveFactSheet, build_fact_sheet
from app.dashboard.model import DashboardPeriod
from app.export.contracts import ExportPayload, build_export_payload
from app.export.package import PackageManifest, build_executive_package
from app.export.verify import PackageVerification, verify_package


@dataclass(frozen=True)
class PipelineResult:
    period: DashboardPeriod
    fact_sheet: ExecutiveFactSheet
    payload: ExportPayload
    manifest: PackageManifest
    verification: PackageVerification


def run_executive_pipeline(
    period: DashboardPeriod,
    output_dir: str | Path,
    prepare: Callable[[DashboardPeriod], DashboardPeriod] | None = None,
) -> PipelineResult:
    validated = prepare(period) if prepare else period
    fact_sheet = build_fact_sheet(validated)
    payload = build_export_payload(fact_sheet)
    manifest = build_executive_package(payload, output_dir)
    verification = verify_package(output_dir)
    return PipelineResult(validated, fact_sheet, payload, manifest, verification)


def run_history(
    periods: Iterable[DashboardPeriod],
    output_root: str | Path,
) -> tuple[PipelineResult, ...]:
    root = Path(output_root)
    return tuple(
        run_executive_pipeline(period, root / period.period)
        for period in periods
    )
