from app.review.rc1_review import review_counts


def test_review_accepts_non_increasing_pipeline_counts() -> None:
    review = review_counts(100, 100, 98, 98)
    assert not review.blocking
    assert review.findings == ()


def test_review_blocks_count_increase() -> None:
    review = review_counts(100, 101, 101, 101)
    assert review.blocking
    assert {item.code for item in review.findings} == {"COUNT-001"}
