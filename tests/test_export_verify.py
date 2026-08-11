from app.dashboard.fact_sheet import build_fact_sheet
from app.dashboard.model import DashboardPeriod
from app.export.contracts import build_export_payload
from app.export.package import build_executive_package
from app.export.verify import verify_package


def test_verify_package_accepts_untouched_outputs(tmp_path) -> None:
    period = DashboardPeriod("2026-Q2", 100, 10, 5, 80, 5, 0.80, 0.05, 0.10, 0.05, True, (), "EV-01")
    build_executive_package(build_export_payload(build_fact_sheet(period)), tmp_path)
    result = verify_package(tmp_path)
    assert result.valid is True
    assert all(item.exists and item.hash_matches for item in result.files)


def test_verify_package_detects_modified_file(tmp_path) -> None:
    period = DashboardPeriod("2026-Q2", 100, 10, 5, 80, 5, 0.80, 0.05, 0.10, 0.05, True, (), "EV-01")
    build_executive_package(build_export_payload(build_fact_sheet(period)), tmp_path)
    target = tmp_path / "siap_rtc_ejecutivo.xlsx"
    target.write_bytes(target.read_bytes() + b"tampered")
    result = verify_package(tmp_path)
    assert result.valid is False
    changed = next(item for item in result.files if item.filename == target.name)
    assert changed.exists is True
    assert changed.hash_matches is False
