"""
test_837_004010X096A1.py
"""
import pytest
from tests.support import assert_eq_model, resources_directory
import os


@pytest.fixture
def resource_path() -> str:
    return os.path.join(resources_directory, "837_004010X096A1")


@pytest.mark.parametrize(
    "file_name",
    [
        "automobile-accident.837",
        "homeowners.837",
        "institutional-ppo-repriced.837",
        "institutional.837",
        "workers-compensation.837",
    ],
)
def test_837i_model(resource_path, file_name: str):
    x12_file_path = os.path.join(resource_path, file_name)
    assert os.path.exists(x12_file_path)
    assert_eq_model(x12_file_path)
