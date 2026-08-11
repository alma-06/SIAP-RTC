from app.pipeline.indicators import build_indicators
from app.pipeline.reconcile import ReconciliationResult


def test_build_indicators_calculates_counts_rates_and_net_change() -> None:
    result = ReconciliationResult(
        decisions=(),
        previous_count=100,
        current_count=110,
        unchanged_count=90,
        added_count=20,
        removed_count=10,
        modified_count=10,
    )
    indicators = build_indicators(result)
    assert indicators.net_change == 10
    assert indicators.retention_rate == 0.90
    assert indicators.added_rate == 20 / 110
    assert indicators.removed_rate == 0.10
    assert indicators.modified_rate == 10 / 110


def test_zero_denominators_return_none() -> None:
    result = ReconciliationResult((), 0, 0, 0, 0, 0, 0)
    indicators = build_indicators(result)
    assert indicators.retention_rate is None
    assert indicators.added_rate is None
    assert indicators.removed_rate is None
    assert indicators.modified_rate is None
