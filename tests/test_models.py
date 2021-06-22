"""
test_models.py

Tests X12 Base Models
"""
from x12.models import (
    X12BaseSegmentModel,
    X12Delimiters,
)
from typing import List, Optional
import datetime
import pytest


@pytest.fixture
def x12_mock_model():
    """
    :return:A Mock model which extends X12BaseModel
    """

    class MockModel(X12BaseSegmentModel):
        """
        A simple model used to test X12BaseModel features.
        """

        first_name: str
        last_name: str
        address: Optional[List[str]]
        birth_date: Optional[datetime.date]

    fields = {
        "delimiters": {
            "element_separator": "*",
            "repetition_separator": "^",
            "segment_terminator": "~",
        },
        "segment_name": "MCK",
        "first_name": "JOHN",
        "last_name": "DOE",
        "address": ["1400 ANYHOO LANE", "PLEASANTVILLE", "SC", "90210"],
        "birth_date": datetime.date(year=1980, month=1, day=1),
    }

    return MockModel(**fields)


def test_x12(x12_mock_model):
    """
    Tests the X12BaseModel's x12() method
    """
    assert (
        x12_mock_model.x12()
        == "MCK*JOHN*DOE*1400 ANYHOO LANE^PLEASANTVILLE^SC^90210*19800101~"
    )

    x12_mock_model.address = None
    assert x12_mock_model.x12() == "MCK*JOHN*DOE**19800101~"

    x12_mock_model.address = ["1400 ANYHOO LANE", "PLEASANTVILLE", "SC", "90210"]
    x12_mock_model.birth_date = None
    assert (
        x12_mock_model.x12() == "MCK*JOHN*DOE*1400 ANYHOO LANE^PLEASANTVILLE^SC^90210~"
    )


def test_x12_delimiter_defaults():
    x12_delimiters: X12Delimiters = X12Delimiters()
    assert x12_delimiters.component_separator == ":"
    assert x12_delimiters.element_separator == "*"
    assert x12_delimiters.repetition_separator == "^"
    assert x12_delimiters.segment_terminator == "~"
