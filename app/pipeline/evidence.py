from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class EvidenceSource:
    filename: str
    sha256: str
    period: str


@dataclass(frozen=True)
class EvidenceManifest:
    evidence_id: str
    metric: str
    methodology: str
    sources: tuple[EvidenceSource, ...]
    warnings: tuple[str, ...]


def file_sha256(path: str | Path) -> str:
    digest = sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_evidence_manifest(
    evidence_id: str,
    metric: str,
    methodology: str,
    source_files: Iterable[tuple[str | Path, str]],
    warnings: Iterable[str] = (),
) -> EvidenceManifest:
    sources = tuple(
        EvidenceSource(Path(path).name, file_sha256(path), period)
        for path, period in source_files
    )
    return EvidenceManifest(evidence_id, metric, methodology, sources, tuple(warnings))


def write_evidence_manifest(manifest: EvidenceManifest, path: str | Path) -> None:
    payload = asdict(manifest)
    Path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
