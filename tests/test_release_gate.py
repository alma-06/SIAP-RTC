from app.release.release_gate import ReleaseInputs, ReleaseStatus, evaluate_release


def base(**kwargs):
    values = dict(
        version="0.1.0",
        commit="abc123",
        run_id="RC1-001",
        master_record="master.json",
        manifest_verified=True,
        technical_opinion="VALIDADO",
        institutional_review="CONFORMING",
        scope="2026-Q2",
    )
    values.update(kwargs)
    return ReleaseInputs(**values)


def test_complete_release_is_allowed() -> None:
    assert evaluate_release(base()) == ReleaseStatus.RELEASED


def test_unverified_manifest_blocks_release() -> None:
    assert evaluate_release(base(manifest_verified=False)) == ReleaseStatus.BLOCKED


def test_institutional_review_must_be_conforming() -> None:
    assert evaluate_release(base(institutional_review="OBSERVED")) == ReleaseStatus.BLOCKED
