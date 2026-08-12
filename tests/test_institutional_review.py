from app.validation.institutional_review import InstitutionalReview, ReviewStatus, evaluate_review


def complete(**kwargs):
    values = dict(
        technical_complete=True,
        documentary_complete=True,
        integrity_ok=True,
        reconciliation_ok=True,
        criterion78_ok=True,
        findings_resolved=True,
    )
    values.update(kwargs)
    return InstitutionalReview(**values)


def test_complete_review_is_conforming() -> None:
    assert evaluate_review(complete()) == ReviewStatus.CONFORMING


def test_observations_are_not_conforming() -> None:
    assert evaluate_review(complete(observations=("OBS-001",))) == ReviewStatus.OBSERVED


def test_missing_critical_control_blocks_review() -> None:
    assert evaluate_review(complete(integrity_ok=False)) == ReviewStatus.BLOCKED
