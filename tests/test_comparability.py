from app.reconciliation.comparability import PeriodMethodology, validate_period_comparability


def test_equal_methodology_is_comparable() -> None:
    result = validate_period_comparability((
        PeriodMethodology("2026-Q1", "CRT-2026", "M1", ("campaign", "version")),
        PeriodMethodology("2026-Q2", "CRT-2026", "M1", ("campaign", "version")),
    ))
    assert result.comparable is True
    assert result.reasons == ()


def test_different_universe_or_methodology_blocks_comparison() -> None:
    result = validate_period_comparability((
        PeriodMethodology("2026-Q1", "CRT-A", "M1", ("campaign",)),
        PeriodMethodology("2026-Q2", "CRT-B", "M2", ("campaign", "version")),
    ))
    assert result.comparable is False
    assert len(result.reasons) == 3
