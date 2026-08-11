from pathlib import Path


def test_acceptance_matrix_contains_critical_scenarios() -> None:
    path = Path("docs/validation/F2-06-acceptance-matrix.md")
    text = path.read_text(encoding="utf-8")
    for scenario in ["AT-01", "AT-03", "AT-07", "AT-11", "AT-13", "AT-15"]:
        assert scenario in text
    assert "Criterio 78" in text
    assert "SHA-256" in text
