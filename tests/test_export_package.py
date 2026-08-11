import json

from app.dashboard.fact_sheet import build_fact_sheet
from app.dashboard.model import DashboardPeriod
from app.export.contracts import build_export_payload
from app.export.package import build_executive_package


def test_build_executive_package_creates_outputs_and_hash_manifest(tmp_path) -> None:
    period = DashboardPeriod("2026-Q2", 100, 10, 5, 80, 5, 0.80, 0.05, 0.10, 0.05, True, (), "EV-01")
    payload = build_export_payload(build_fact_sheet(period))
    manifest = build_executive_package(payload, tmp_path)

    assert manifest.period == "2026-Q2"
    assert manifest.evidence_id == "EV-01"
    assert len(manifest.files) == 3
    assert all(len(value) == 64 for value in manifest.sha256.values())

    saved = json.loads((tmp_path / "manifest.json").read_text(encoding="utf-8"))
    assert saved["evidence_id"] == "EV-01"
