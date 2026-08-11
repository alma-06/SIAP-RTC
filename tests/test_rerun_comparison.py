from app.review.re_run_comparison import compare_runs


def test_compare_runs_reports_metric_deltas() -> None:
    comparison = compare_runs("RC1", "RC2", {"records": 100, "spots": 40}, {"records": 98, "spots": 42})
    assert [(item.name, item.delta) for item in comparison.metrics] == [("records", -2), ("spots", 2)]
    assert comparison.previous_run_id == "RC1"
    assert comparison.current_run_id == "RC2"
