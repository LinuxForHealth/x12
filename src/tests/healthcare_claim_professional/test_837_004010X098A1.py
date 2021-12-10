"""
test_837_004010X098A1.py
"""
import pytest
from tests.support import assert_eq_model, resources_directory
import os


@pytest.fixture
def resource_path() -> str:
    return os.path.join(resources_directory, "837_004010X098A1")


@pytest.mark.parametrize(
    "file_name",
    [
        "coordination-of-benefits.837",
        "dependent-commercial-insurance-02.837",
        "patient-is-dependent.837",
        "dependent-commercial-insurance-01.837",
        "dependent-commercial-insurance-03.837",
        "patient-is-subscriber.837",
    ],
)
def test_837_model(resource_path, file_name: str):
    x12_file_path = os.path.join(resource_path, file_name)
    assert os.path.exists(x12_file_path)
    assert_eq_model(x12_file_path)
