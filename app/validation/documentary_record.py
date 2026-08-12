from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path


@dataclass(frozen=True)
class DocumentaryRecord:
    evidence_id: str
    document_type: str
    title: str
    reference: str
    date: str
    source: str
    file_path: str
    sha256: str
    supports: tuple[str, ...] = ()
    observations: tuple[str, ...] = ()

    def to_dict(self) -> dict:
        return asdict(self)


class DocumentaryRegister:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def list(self) -> tuple[DocumentaryRecord, ...]:
        if not self.path.exists():
            return ()
        data = json.loads(self.path.read_text(encoding="utf-8"))
        return tuple(DocumentaryRecord(**item) for item in data.get("documents", []))

    def add(self, record: DocumentaryRecord) -> DocumentaryRecord:
        records = list(self.list())
        if any(item.evidence_id == record.evidence_id for item in records):
            raise ValueError(f"Evidencia documental duplicada: {record.evidence_id}")
        if not record.file_path or not record.sha256:
            raise ValueError("La evidencia debe identificar archivo y SHA-256")
        records.append(record)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps({"documents": [item.to_dict() for item in records]}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return record
