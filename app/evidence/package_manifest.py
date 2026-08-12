from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import hashlib
import json


@dataclass(frozen=True)
class EvidenceItem:
    relative_path: str
    sha256: str
    size_bytes: int


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_manifest(root: str | Path) -> tuple[EvidenceItem, ...]:
    base = Path(root)
    items: list[EvidenceItem] = []
    for path in sorted(p for p in base.rglob("*") if p.is_file()):
        items.append(
            EvidenceItem(
                relative_path=path.relative_to(base).as_posix(),
                sha256=sha256_file(path),
                size_bytes=path.stat().st_size,
            )
        )
    return tuple(items)


def save_manifest(root: str | Path, destination: str | Path) -> None:
    items = build_manifest(root)
    payload = {"files": [asdict(item) for item in items]}
    Path(destination).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
