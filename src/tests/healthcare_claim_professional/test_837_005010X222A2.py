"""
test_837_005010XX222A2.py
"""
import pytest
from tests.support import assert_eq_model, resources_directory
import os


@pytest.fixture
def resource_path() -> str:
    return os.path.join(resources_directory, "837_005010X222A2")


@pytest.mark.parametrize(
    "file_name",
    [
        "demo.ambulance.example5.837",
        "demo.autoaccident.837",
        "demo.cob.2ndary.example4.837",
        "demo.cob.example3.A.837",
        "demo.cob.example3.B.837",
        "demo.cob.example3.C.837",
        "demo.cob.example4.837",
        "demo.drug.example10.1.837",
        "demo.drug.example10.2.837",
        "demo.drug.example10.3.837",
        "demo.example6.837",
        "demo.example7.837",
        "demo.example8.837",
        "demo.example9.837",
        "demo.example11.837",
        "demo.example12.837",
        "demo.example1.837",
        "demo.example2.837",
    ],
)
def test_837_model(resource_path, file_name: str):
    x12_file_path = os.path.join(resource_path, file_name)
    assert os.path.exists(x12_file_path)
    assert_eq_model(x12_file_path)
