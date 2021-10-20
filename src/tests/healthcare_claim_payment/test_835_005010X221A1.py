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


def test_835_properties(resource_path: str):
    """
    Test 835 properties

    :param resource_path: The path to the directory containing x12 test files
    """
    x12_file = os.path.join(resource_path, "managed-care.835")
    assert os.path.exists(x12_file)

    with X12ModelReader(x12_file) as r:
        model_result = [m for m in r.models()]
        assert len(model_result) == 1

        model = model_result[0]

        n1_segment = model.payer["n1_segment"]
        assert n1_segment["name"] == "RUSHMORE LIFE"

        n1_segment = model.payee["n1_segment"]
        assert n1_segment["name"] == "ACME MEDICAL CENTER"

        claim_data = model.claim
        assert "clp_segment" in claim_data
        assert "cas_segment" in claim_data
        assert "loop_2110" in claim_data
