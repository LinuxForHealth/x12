"""
test_837_005010XX223A3.py
"""
import pytest
from tests.support import assert_eq_model, resources_directory
import os


@pytest.fixture
def resource_path() -> str:
    return os.path.join(resources_directory, "837_005010X223A3")


@pytest.mark.parametrize(
    "file_name",
    [
        "institutional-claim.837i",
        "out-of-network-repriced-claim.837i",
        "ppo-repriced-claim.837i",
        "two-claims-single-provider.837i",
    ],
)
def test_837i_model(resource_path, file_name: str):
    x12_file_path = os.path.join(resource_path, file_name)
    assert os.path.exists(x12_file_path)
    assert_eq_model(x12_file_path)
