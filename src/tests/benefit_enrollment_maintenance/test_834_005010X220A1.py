"""
test_834_005010X220A1.py

Tests the benefit enrollment (834) transaction
"""
from tests.support import assert_eq_model, resources_directory
import os
import pytest


@pytest.fixture
def resource_path() -> str:
    return os.path.join(resources_directory, "834_005010X220A1")


@pytest.mark.parametrize(
    "file_name",
    ["enroll-employee-multiple-products.834"],
)
def test_834_model(resource_path, file_name: str):

    x12_file_path = os.path.join(resource_path, file_name)
    assert os.path.exists(x12_file_path)
    assert_eq_model(x12_file_path)
