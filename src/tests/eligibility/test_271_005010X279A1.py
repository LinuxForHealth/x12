"""
Tests use-cases for the 271 005010X279A1 (Eligibility Benefit Response) transaction
"""
import pytest
from tests.support import assert_eq_model, resources_directory
import os


@pytest.fixture
def resource_path() -> str:
    return os.path.join(resources_directory, "271_005010X279A1")


@pytest.mark.parametrize(
    "file_name",
    [
        "subscriber-health-benefit-check.271",
        "subscriber-health-benefit-check-error.271",
        "dependent-health-benefit-check.271",
    ],
)
def test_271_model(resource_path, file_name: str):
    x12_file_path = os.path.join(resource_path, file_name)
    assert os.path.exists(x12_file_path)
    assert_eq_model(x12_file_path)
