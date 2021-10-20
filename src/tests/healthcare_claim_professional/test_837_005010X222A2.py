"""
test_837_005010XX222A2.py
"""
from x12.io import X12ModelReader
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
    ],
)
def test_837_model(resource_path, file_name: str):
    x12_file_path = os.path.join(resource_path, file_name)
    assert os.path.exists(x12_file_path)
    assert_eq_model(x12_file_path)


# def test_837_subscriber_properties(resource_path: str):
#     """
#     Test 837 properties where the patient is the subscriber
#
#     :param resource_path: The path to the directory containing x12 test files
#     """
#     x12_file = os.path.join(resource_path, "example.3.1.2.encounter.837")
#     assert os.path.exists(x12_file)
#
#     with X12ModelReader(x12_file) as r:
#         model_result = [m for m in r.models()]
#         assert len(model_result) == 1
#
#         model = model_result[0]
#
#         nm1_segment = model.patient["loop_2010ba"]["nm1_segment"]
#         assert nm1_segment["name_last_or_organization_name"] == "SMITH"
#         assert nm1_segment["name_first"] == "TED"
#
#         claim_data = model.claim
#         assert claim_data["clm_segment"] is not None
#         assert len(claim_data["sv1_segment"]) == 4


# def test_837_dependent_properties(resource_path: str):
#     """
#     Test 837 properties where the patient is not the subscriber
#
#     :param resource_path: The path to the directory containing x12 test files
#     """
#     x12_file = os.path.join(resource_path, "commercial-health-insurance.837")
#     assert os.path.exists(x12_file)
#
#     with X12ModelReader(x12_file) as r:
#         model_result = [m for m in r.models()]
#         assert len(model_result) == 1
#
#         model = model_result[0]
#         assert "loop_2300" not in model
#
#         nm1_segment = model.patient["loop_2010ca"]["nm1_segment"]
#         assert nm1_segment["name_last_or_organization_name"] == "SMITH"
#         assert nm1_segment["name_first"] == "TED"
#
#         claim_data = model.claim
#         assert claim_data["clm_segment"] is not None
#         assert len(claim_data["sv1_segment"]) == 4
