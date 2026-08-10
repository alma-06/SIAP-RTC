from app.reconciliation.period_series import PeriodReconciliation, build_historical_series
from app.reconciliation.summary import ReconciliationSummary


def summary(additions: int, removals: int, persistence: int, modifications: int) -> ReconciliationSummary:
    return ReconciliationSummary(
        total_compared=additions + removals + persistence + modifications,
        additions=additions,
        removals=removals,
        persistence=persistence,
        modifications=modifications,
    )


def test_build_historical_series_preserves_period_order() -> None:
    series = build_historical_series(
        (
            PeriodReconciliation("2026-Q1", summary(2, 1, 7, 1)),
            PeriodReconciliation("2026-Q2", summary(3, 2, 8, 2)),
        )
    )
    assert series.total_periods == 2
    assert [item.period for item in series.periods] == ["2026-Q1", "2026-Q2"]
    assert series.periods[1].summary.additions == 3
