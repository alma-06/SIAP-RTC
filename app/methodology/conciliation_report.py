from __future__ import annotations

from dataclasses import dataclass

from app.methodology.conciliation_case import ConciliationCase


@dataclass(frozen=True)
class ConciliationReport:
    title: str
    sections: tuple[tuple[str, tuple[tuple[str, object], ...]], ...]

    def to_markdown(self) -> str:
        lines = [f"# {self.title}", ""]
        for heading, rows in self.sections:
            lines.extend([f"## {heading}", ""])
            for label, value in rows:
                lines.append(f"- **{label}:** {value}")
            lines.append("")
        return "\n".join(lines).rstrip() + "\n"


def build_conciliation_report(case: ConciliationCase) -> ConciliationReport:
    evidence = case.evidence_summary()
    result = case.calculate()
    return ConciliationReport(
        title=f"Expediente de conciliación — {case.case_id}",
        sections=(
            ("Identificación", tuple((key, evidence[key]) for key in (
                "case_id", "period", "source_file", "source_hash"
            ))),
            ("Universo de radiodifusoras", tuple((key, evidence[key]) for key in (
                "universe_id", "broadcaster_count", "universe_source",
                "universe_cutoff_date", "universe_methodology"
            ))),
            ("Parámetros y cálculo", (
                ("Impactos", case.impacts),
                ("Duración estándar (segundos)", case.standard_spot_seconds),
                ("Fórmula", "impactos × radiodifusoras × duración estándar"),
                ("Segundos calculados", result.total_seconds),
                ("Resultado [h]:mm:ss", result.elapsed_time),
            )),
            ("Interpretación y limitaciones", (
                ("Interpretación", result.interpretation),
                ("Notas", case.notes or "Sin notas adicionales."),
            )),
        ),
    )
