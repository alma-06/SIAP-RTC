from app.reconciliation.source_reconciliation import ReconciliationStatus, reconcile_identities


def test_reconciliation_distinguishes_new_existing_and_source_duplicates() -> None:
    items, summary = reconcile_identities(
        ["A", "B", "A", "C"],
        {"B"},
    )
    assert [i.status for i in items] == [
        ReconciliationStatus.NEW,
        ReconciliationStatus.EXISTING,
        ReconciliationStatus.EXISTING,
        ReconciliationStatus.NEW,
    ]
    assert summary.source_count == 4
    assert summary.new_count == 2
    assert summary.existing_count == 2
    assert summary.duplicate_source_count == 1


def test_reconciliation_does_not_mutate_history() -> None:
    history = {"A"}
    reconcile_identities(["B"], history)
    assert history == {"A"}
