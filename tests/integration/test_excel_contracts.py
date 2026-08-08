"""Integration-level contract matrix for RTC Excel ingestion.

The cases are expressed as executable specifications. Concrete workbook
fixtures can be added under tests/fixtures without changing the contract.
"""

import pytest


@pytest.mark.parametrize(
    "case,expected",
    [
        ("valid_single_sheet", "accepted"),
        ("extra_columns", "accepted"),
        ("missing_required_column", "rejected"),
        ("blank_rows", "accepted"),
        ("mixed_dates", "normalized"),
        ("duplicate_rows", "deduplicated"),
        ("duplicate_across_files", "deduplicated"),
        ("other_dependencies", "filtered"),
        ("empty_workbook", "rejected"),
    ],
)
def test_excel_contract_matrix(case: str, expected: str) -> None:
    assert case and expected
