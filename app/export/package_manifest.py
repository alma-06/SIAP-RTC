from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


@dataclass(frozen=True)
class PackageFile:
    path: str
    size: int
    sha256: str


def _hash_file(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_package_manifest(root: str | Path, evidence_id: str, period: str) -> dict[str, object]:
    root_path = Path(root)
    files = []
    for path in sorted(p for p in root_path.rglob("*") if p.is_file() and p.name != "PackageManifest.json"):
        files.append(asdict(PackageFile(str(path.relative_to(root_path)), path.stat().st_size, _hash_file(path))))
    return {
        "package": "SIAP-RTC",
        "period": period,
        "evidence_id": evidence_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "files": files,
    }


def write_package_manifest(root: str | Path, evidence_id: str, period: str) -> Path:
    root_path = Path(root)
    manifest_path = root_path / "PackageManifest.json"
    manifest = build_package_manifest(root_path, evidence_id, period)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest_path


def verify_package(root: str | Path) -> tuple[bool, list[str]]:
    root_path = Path(root)
    manifest_path = root_path / "PackageManifest.json"
    if not manifest_path.exists():
        return False, ["PackageManifest.json no existe"]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    errors: list[str] = []
    expected = {item["path"]: item for item in manifest.get("files", [])}
    for relative, item in expected.items():
        path = root_path / relative
        if not path.exists():
            errors.append(f"Falta archivo: {relative}")
            continue
        if path.stat().st_size != item["size"]:
            errors.append(f"Tamaño inconsistente: {relative}")
        if _hash_file(path) != item["sha256"]:
            errors.append(f"SHA-256 inconsistente: {relative}")
    actual = {str(p.relative_to(root_path)) for p in root_path.rglob("*") if p.is_file() and p.name != "PackageManifest.json"}
    for relative in sorted(actual - set(expected)):
        errors.append(f"Archivo no manifestado: {relative}")
    return not errors, errors


def zip_package(root: str | Path, output: str | Path) -> Path:
    root_path = Path(root)
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output_path, "w", ZIP_DEFLATED) as archive:
        for path in sorted(p for p in root_path.rglob("*") if p.is_file()):
            archive.write(path, path.relative_to(root_path))
    return output_path
