from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class IntegrityIssue:
    code: str
    path: str


@dataclass(frozen=True)
class IntegrityReport:
    valid: bool
    issues: tuple[IntegrityIssue, ...]


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_complete_package(package_dir: str | Path) -> IntegrityReport:
    root = Path(package_dir)
    manifest_path = root / "manifest.json"
    if not manifest_path.is_file():
        return IntegrityReport(False, (IntegrityIssue("MANIFEST-MISSING", "manifest.json"),))

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected = manifest.get("sha256", {})
    issues: list[IntegrityIssue] = []

    for relative, expected_hash in expected.items():
        path = root / relative
        if not path.is_file():
            issues.append(IntegrityIssue("FILE-MISSING", relative))
        elif _sha256(path) != expected_hash:
            issues.append(IntegrityIssue("HASH-MISMATCH", relative))

    actual = {
        p.relative_to(root).as_posix()
        for p in root.rglob("*")
        if p.is_file() and p != manifest_path
    }
    for relative in sorted(actual - set(expected)):
        issues.append(IntegrityIssue("FILE-UNMANIFESTED", relative))

    return IntegrityReport(not issues, tuple(issues))
