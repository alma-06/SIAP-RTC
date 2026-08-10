import pytest

from app.methodology.broadcaster_universe import BroadcasterUniverse


def test_universe_preserves_source_and_cutoff() -> None:
    universe = BroadcasterUniverse(
        universe_id="CRT-2026-Q2",
        total_stations=1377,
        source="Base de estaciones AM/FM de la CRT",
        cutoff_date="2026-06-30",
        methodology="Conteo de estaciones activas con corte trimestral",
        source_file="estaciones_q2_2026.xlsx",
    )
    params = universe.as_criterion_78_parameters()
    assert params.broadcaster_count == 1377
    assert params.parameter_source == universe.source
    assert params.cutoff_date == universe.cutoff_date


@pytest.mark.parametrize("field", ["source", "cutoff_date", "methodology"])
def test_required_traceability_fields_are_required(field: str) -> None:
    values = {
        "universe_id": "U1",
        "total_stations": 1,
        "source": "fuente",
        "cutoff_date": "2026-06-30",
        "methodology": "conteo",
    }
    values[field] = ""
    with pytest.raises(ValueError):
        BroadcasterUniverse(**values)
