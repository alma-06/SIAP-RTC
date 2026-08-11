import json

from app.pipeline.evidence import build_evidence_manifest, write_evidence_manifest


def test_evidence_manifest_records_source_hash_and_methodology(tmp_path) -> None:
    source = tmp_path / "rtc.xlsx"
    source.write_bytes(b"rtc-source")
    manifest = build_evidence_manifest(
        "EV-2026-Q2-001",
        "registros de pauta",
        "conteo de registros CAM. SEN. después de normalización y deduplicación exacta",
        [(source, "2026-Q2")],
        ["No acredita transmisión efectiva"],
    )
    output = tmp_path / "evidence.json"
    write_evidence_manifest(manifest, output)
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["evidence_id"] == "EV-2026-Q2-001"
    assert payload["sources"][0]["filename"] == "rtc.xlsx"
    assert len(payload["sources"][0]["sha256"]) == 64
    assert payload["warnings"] == ["No acredita transmisión efectiva"]
