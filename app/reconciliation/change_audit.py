from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Mapping

from app.reconciliation.content_diff import ContentComparison, ContentStatus


@dataclass(frozen=True)
class ChangeAuditEntry:
    identity_hash: str
    source_file: str
    previous_source_file: str | None
    detected_at: str
    field: str
    previous_value: object
    current_value: object
    change_type: str = "CONTENT_CHANGE"
    import_batch_id: str | None = None


def build_change_audit_entries(
    comparison: ContentComparison,
    source_file: str,
    previous_source_file: str | None = None,
    import_batch_id: str | None = None,
    detected_at: str | None = None,
) -> tuple[ChangeAuditEntry, ...]:
    if comparison.status is not ContentStatus.CHANGED:
        return ()
    timestamp = detected_at or datetime.now(timezone.utc).isoformat()
    return tuple(
        ChangeAuditEntry(
            identity_hash=comparison.identity_hash,
            source_file=source_file,
            previous_source_file=previous_source_file,
            detected_at=timestamp,
            field=difference.field,
            previous_value=difference.previous,
            current_value=difference.current,
            import_batch_id=import_batch_id,
        )
        for difference in comparison.differences
    )
