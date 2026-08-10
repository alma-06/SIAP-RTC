from app.reconciliation.summary import summarize_reconciliation
from app.reconciliation.temporal_reconciliation import TemporalStatus, TemporalChange


def test_summary_counts_and_rates() -> None:
    changes = (
        TemporalChange("A", TemporalStatus.ADDITION),
        TemporalChange("B", TemporalStatus.REMOVAL),
        TemporalChange("C", TemporalStatus.PERSISTENCE),
        TemporalChange("D", TemporalStatus.PERSISTENCE),
        TemporalChange("E", TemporalStatus.MODIFICATION, ("version",)),
    )
    summary = summarize_reconciliation(changes)
    assert summary.total_compared == 5
    assert summary.additions == 1
    assert summary.removals == 1
    assert summary.persistence == 2
    assert summary.modifications == 1
    assert summary.match_rate == 0.4
    assert summary.change_rate == 0.2
    assert summary.addition_rate == 0.2
    assert summary.removal_rate == 0.2


def test_empty_summary_is_safe() -> None:
    summary = summarize_reconciliation(())
    assert summary.total_compared == 0
    assert summary.match_rate == 0.0
    assert summary.change_rate == 0.0
