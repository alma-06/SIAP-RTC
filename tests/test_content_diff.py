from app.reconciliation.content_diff import ContentStatus, compare_content


def test_content_difference_reports_changed_fields() -> None:
    result = compare_content(
        "A",
        {"campaign": "X", "version": "01", "channel": "AM"},
        {"campaign": "X", "version": "02", "channel": "AM"},
        ("campaign", "version", "channel"),
    )
    assert result.status is ContentStatus.CHANGED
    assert len(result.differences) == 1
    assert result.differences[0].field == "version"
    assert result.differences[0].previous == "01"
    assert result.differences[0].current == "02"


def test_identical_content_has_no_differences() -> None:
    result = compare_content(
        "A",
        {"campaign": "X", "version": "01"},
        {"campaign": "X", "version": "01"},
        ("campaign", "version"),
    )
    assert result.status is ContentStatus.IDENTICAL
    assert result.differences == ()
