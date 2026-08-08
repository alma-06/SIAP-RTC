from __future__ import annotations

from dataclasses import dataclass
import re
import unicodedata

from app.processing.rtc_reader import NormalizedRTCRecord


TARGET = "CAM SEN"


def normalize_dependency(value: object) -> str:
    text = "" if value is None else str(value)
    text = unicodedata.normalize("NFKC", text).upper().strip()
    text = text.replace("CÁM.", "CAM").replace("CÁMARA", "CAMARA")
    text = re.sub(r"[.\-_]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


@dataclass(frozen=True)
class FilterDecision:
    accepted: bool
    reason: str
    record: NormalizedRTCRecord


class CamSenFilter:
    def apply(self, record: NormalizedRTCRecord) -> FilterDecision:
        raw = record.values.get("dependencia_cam_sen", "")
        normalized = normalize_dependency(raw)
        accepted = normalized in {TARGET, "CAM SENADO", "CAMARA SENADO", "CAMARA DE SENADORES"}
        reason = "CAM_SEN_ACCEPTED" if accepted else "DEPENDENCIA_NO_CAM_SEN"
        return FilterDecision(accepted=accepted, reason=reason, record=record)

    def filter(self, records: list[NormalizedRTCRecord]) -> tuple[list[NormalizedRTCRecord], list[FilterDecision]]:
        accepted: list[NormalizedRTCRecord] = []
        decisions: list[FilterDecision] = []
        for record in records:
            decision = self.apply(record)
            decisions.append(decision)
            if decision.accepted:
                accepted.append(record)
        return accepted, decisions
