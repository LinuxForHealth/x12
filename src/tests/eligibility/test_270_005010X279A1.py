"""
Tests use-cases for the 270 005010X279A1 (Eligibility Inquiry) transaction
"""

from x12.io import X12ModelReader
import pytest
from tests.support import assert_eq_model, resources_directory
import os


@pytest.fixture
def resource_path() -> str:
    return os.path.join(resources_directory, "270_005010X279A1")


@pytest.mark.parametrize(
    "file_name",
    ["dependent-health-benefit-check.270", "subscriber-health-benefit-check.270"],
)
def test_270_model(resource_path, file_name: str):

    x12_file_path = os.path.join(resource_path, file_name)
    assert os.path.exists(x12_file_path)
    assert_eq_model(x12_file_path)
