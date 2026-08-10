from app.reconciliation.temporal_reconciliation import TemporalStatus, reconcile_periods


def test_temporal_reconciliation_classifies_additions_removals_persistence_and_modifications() -> None:
    previous = {
        "A": {"version": "01"},
        "B": {"version": "01"},
        "C": {"version": "01"},
    }
    current = {
        "A": {"version": "02"},
        "B": {"version": "01"},
        "D": {"version": "01"},
    }
    changes = reconcile_periods(previous, current, ("version",))
    by_id = {change.identity_hash: change for change in changes}
    assert by_id["A"].status is TemporalStatus.MODIFICATION
    assert by_id["A"].differences == ("version",)
    assert by_id["B"].status is TemporalStatus.PERSISTENCE
    assert by_id["C"].status is TemporalStatus.REMOVAL
    assert by_id["D"].status is TemporalStatus.ADDITION
