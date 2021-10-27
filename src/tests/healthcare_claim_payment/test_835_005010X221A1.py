"""
test_835_005010XX221A1.py
"""
from x12.io import X12ModelReader
import pytest
from tests.support import assert_eq_model, resources_directory
import os


@pytest.fixture
def resource_path() -> str:
    return os.path.join(resources_directory, "835_005010X221A1")


@pytest.mark.parametrize(
    "file_name",
    ["managed-care.835"],
)
def test_835_model(resource_path, file_name: str):
    x12_file_path = os.path.join(resource_path, file_name)
    assert os.path.exists(x12_file_path)
    assert_eq_model(x12_file_path)
