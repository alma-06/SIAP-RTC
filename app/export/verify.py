from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FileVerification:
    filename: str
    exists: bool
    hash_matches: bool


@dataclass(frozen=True)
class PackageVerification:
    valid: bool
    files: tuple[FileVerification, ...]


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_package(package_dir: str | Path) -> PackageVerification:
    directory = Path(package_dir)
    manifest_path = directory / "manifest.json"
    if not manifest_path.exists():
        return PackageVerification(False, ())

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    results: list[FileVerification] = []
    for filename, expected_hash in manifest.get("sha256", {}).items():
        path = directory / filename
        exists = path.is_file()
        matches = exists and _sha256(path) == expected_hash
        results.append(FileVerification(filename, exists, matches))

    valid = bool(results) and all(item.exists and item.hash_matches for item in results)
    return PackageVerification(valid, tuple(results))
