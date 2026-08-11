from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path

from app.export.contracts import ExportPayload
from app.export.docx import export_docx
from app.export.pptx import export_pptx
from app.export.xlsx import export_xlsx


@dataclass(frozen=True)
class PackageManifest:
    title: str
    period: str
    evidence_id: str
    files: tuple[str, ...]
    sha256: dict[str, str]


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_executive_package(payload: ExportPayload, output_dir: str | Path) -> PackageManifest:
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)

    xlsx = export_xlsx(payload, directory / "siap_rtc_ejecutivo.xlsx")
    docx = export_docx(payload, directory / "siap_rtc_ejecutivo.docx")
    pptx = export_pptx(payload, directory / "siap_rtc_ejecutivo.pptx")

    files = tuple(path.name for path in (xlsx, docx, pptx))
    hashes = {path.name: _sha256(path) for path in (xlsx, docx, pptx)}
    manifest = PackageManifest(payload.title, payload.period, payload.evidence_id, files, hashes)

    (directory / "manifest.json").write_text(
        json.dumps(asdict(manifest), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return manifest
