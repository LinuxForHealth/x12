"""
test_api.py

Tests the optional Fast API x12/endpoint
"""
import pytest
from linuxforhealth.x12.api import app
from typing import Dict

# determine if we need to skip the API tests, based on the installation
try:
    from fastapi.testclient import TestClient

    is_fastapi_disabled = False
except ImportError:
    is_fastapi_disabled = True


@pytest.fixture()
def api_test_client() -> TestClient:
    """Returns the API test client fixture"""
    test_client = TestClient(app)
    return test_client


@pytest.fixture
def mock_x12_payload(simple_270_with_new_lines: str) -> Dict:
    x12_payload = {"x12": simple_270_with_new_lines}
    return x12_payload


@pytest.mark.skipif(is_fastapi_disabled, reason="X12 API endpoint is not enabled")
@pytest.mark.parametrize(
    "header, expected_first_value",
    [
        # the response payload and resulting "first value" varies based on the request header
        (None, "header"),
        ("models", "header"),
        ("Models", "header"),
        ("MODELS", "header"),
        ("segments", "ISA"),
        ("Segments", "ISA"),
        ("SEGMENTS", "ISA"),
    ],
)
def test_x12_ok(mock_x12_payload, api_test_client, header, expected_first_value):
    """
    Tests the x12 segment response with parameterized header and expected values.
    :param mock_x12_payload: The X12 request payload for the test
    :param api_test_client: The configured Fast API test client
    :param header: The parameterized header value
    :param expected_first_value: The parameterized first value
    """
    api_response = api_test_client.post(
        "/x12", json=mock_x12_payload, headers={"LFH-X12-RESPONSE": header}
    )
    assert api_response.status_code == 200
    assert expected_first_value in api_response.json()[0]


@pytest.mark.skipif(is_fastapi_disabled, reason="X12 API endpoint is not enabled")
def test_x12_invalid_request(api_test_client, mock_x12_payload):
    """
    Validates that invalid
    :param api_test_client: The configured Fast API test client
    :param mock_x12_payload: The X12 request payload for the test
    """
    api_response = api_test_client.post("/x12", json={"data": mock_x12_payload})
    assert api_response.status_code == 400

    invalid_x12 = list(mock_x12_payload.values())[0].replace(
        "NM1*IL*1*DOE*JOHN****MI*00000000001~", "NM1*FF*1*DOE*JOHN****MI*00000000001~"
    )
    invalid_payload = {"x12": invalid_x12}
    api_response = api_test_client.post("/x12", json=invalid_payload)
    assert api_response.status_code == 400
