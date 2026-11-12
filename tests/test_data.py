"""Every data file must pass the same validation that CI runs."""
from scripts.validate_data import validate_all


def test_data_files_are_valid():
    errors = validate_all()
    assert not errors, "\n".join(errors)
