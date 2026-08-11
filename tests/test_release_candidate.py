from app.release.release_candidate import ReleaseCheck, build_release_candidate_report


def test_release_candidate_is_ready_when_all_blocking_checks_pass() -> None:
    report = build_release_candidate_report(
        "SIAP-RTC v0.1.0-rc1",
        [
            ReleaseCheck("Pruebas críticas", True, True),
            ReleaseCheck("Advertencia no bloqueante", False, False),
        ],
    )
    assert report.ready


def test_release_candidate_is_not_ready_with_blocking_failure() -> None:
    report = build_release_candidate_report(
        "SIAP-RTC v0.1.0-rc1",
        [ReleaseCheck("Matriz de aceptación", False, True)],
    )
    assert not report.ready
