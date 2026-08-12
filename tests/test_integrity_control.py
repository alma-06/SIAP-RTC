from app.validation.integrity_control import verify_complete_package
import hashlib
import json


def _write_manifest(root, mapping):
    (root / "manifest.json").write_text(json.dumps({"sha256": mapping}), encoding="utf-8")


def test_integrity_accepts_complete_package(tmp_path):
    file = tmp_path / "evidence.txt"
    file.write_text("ok", encoding="utf-8")
    digest = hashlib.sha256(file.read_bytes()).hexdigest()
    _write_manifest(tmp_path, {"evidence.txt": digest})
    report = verify_complete_package(tmp_path)
    assert report.valid


def test_integrity_detects_modified_file(tmp_path):
    file = tmp_path / "evidence.txt"
    file.write_text("original", encoding="utf-8")
    digest = hashlib.sha256(file.read_bytes()).hexdigest()
    _write_manifest(tmp_path, {"evidence.txt": digest})
    file.write_text("modified", encoding="utf-8")
    report = verify_complete_package(tmp_path)
    assert not report.valid
    assert report.issues[0].code == "HASH-MISMATCH"


def test_integrity_detects_unmanifested_file(tmp_path):
    file = tmp_path / "evidence.txt"
    file.write_text("ok", encoding="utf-8")
    digest = hashlib.sha256(file.read_bytes()).hexdigest()
    _write_manifest(tmp_path, {"evidence.txt": digest})
    (tmp_path / "extra.txt").write_text("unexpected", encoding="utf-8")
    report = verify_complete_package(tmp_path)
    assert not report.valid
    assert report.issues[0].code == "FILE-UNMANIFESTED"
