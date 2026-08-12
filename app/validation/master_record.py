from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json
from pathlib import Path


@dataclass(frozen=True)
class MasterRecord:
    period: str
    version: str
    run_id: str
    source_files: tuple[str, ...] = ()
    source_sha256: tuple[str, ...] = ()
    structural_profile: str = ""
    preflight: str = ""
    rules: tuple[str, ...] = ()
    reconciliation: str = ""
    criterion78: str = ""
    indicators: tuple[str, ...] = ()
    findings: tuple[str, ...] = ()
    adjustments: tuple[str, ...] = ()
    reruns: tuple[str, ...] = ()
    deliverables: tuple[str, ...] = ()
    evidence_manifest: str = ""
    technical_opinion: str = "NO_VALIDADO"
    notes: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict:
        return asdict(self)

    def save(self, path: str | Path) -> None:
        destination = Path(path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(self.to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    @classmethod
    def load(cls, path: str | Path) -> "MasterRecord":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls(**data)
