from pathlib import Path

from app.export.package_manifest import build_package_manifest, verify_package, write_package_manifest, zip_package


def test_manifest_detects_modified_file_and_zip(tmp_path) -> None:
    root = tmp_path / "package"
    root.mkdir()
    (root / "Informe_Ejecutivo.docx").write_bytes(b"document")
    (root / "SIAP-RTC.xlsx").write_bytes(b"spreadsheet")

    write_package_manifest(root, "EV-2026-Q2", "2026-Q2")
    valid, errors = verify_package(root)
    assert valid
    assert errors == []

    (root / "SIAP-RTC.xlsx").write_bytes(b"changed")
    valid, errors = verify_package(root)
    assert not valid
    assert any("SHA-256 inconsistente" in error for error in errors)

    output = tmp_path / "SIAP-RTC_2026-Q2.zip"
    zip_package(root, output)
    assert output.exists()
    assert output.stat().st_size > 0
