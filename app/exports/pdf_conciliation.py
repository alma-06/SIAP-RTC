from __future__ import annotations

from dataclasses import dataclass

from app.methodology.conciliation_case import ConciliationCase
from app.methodology.conciliation_report import build_conciliation_report


@dataclass(frozen=True)
class PdfConciliationDocument:
    title: str
    markdown_source: str


def build_pdf_conciliation_document(case: ConciliationCase) -> PdfConciliationDocument:
    """Build the canonical content source for PDF rendering.

    PDF rendering is deliberately separated from methodological calculations.
    A renderer can later transform this UTF-8 source into a PDF without
    reimplementing any business rule.
    """
    report = build_conciliation_report(case)
    return PdfConciliationDocument(
        title=report.title,
        markdown_source=report.to_markdown(),
    )
