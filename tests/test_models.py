"""
test_models.py

Tests X12 Base Models
"""
import datetime
from typing import List, Optional

import pytest

from x12.models import X12BaseLoopModel, X12BaseSegmentModel
from x12.segments import Nm1Segment, StSegment


@pytest.fixture()
def x12_mock_loop(x12_delimiters):
    class MockSubLoop(X12BaseLoopModel):
        nm1_segment: Nm1Segment

    """
    :return: A mock X12 Loop with segment data
    """

    class MockLoop(X12BaseLoopModel):
        st_segment: StSegment
        sub_loop: MockSubLoop

    loop_data = {
        "loop_name": "mock_loop",
        "loop_description": "mock loop",
        "st_segment": {
            "delimiters": x12_delimiters.dict(),
            "segment_name": "ST",
            "transaction_set_identifier_code": "270",
            "transaction_set_control_number": "0001",
            "implementation_convention_reference": "005010X279A1",
        },
        "sub_loop": {
            "loop_name": "sub_loop",
            "loop_description": "mock sub loop",
            "nm1_segment": {
                "delimiters": x12_delimiters.dict(),
                "segment_name": "NM1",
                "entity_identifier_code": "PR",
                "entity_type_qualifier": "2",
                "name_last_or_organization_name": "ACME",
                "identification_code_qualifier": "PI",
                "identification_code": "12345",
            },
        },
    }
    return MockLoop(**loop_data)


@pytest.fixture
def x12_mock_model(x12_delimiters):
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
        creation_time: Optional[datetime.time]

    fields = {
        "delimiters": x12_delimiters.dict(),
        "segment_name": "MCK",
        "first_name": "JOHN",
        "last_name": "DOE",
        "address": ["1400 ANYHOO LANE", "PLEASANTVILLE", "SC", "90210"],
        "birth_date": datetime.date(year=1980, month=1, day=1),
        "creation_time": datetime.time(hour=7, minute=5, second=0),
    }

    return MockModel(**fields)


def test_x12_method(x12_mock_model):
    """
    Tests the X12BaseModel's x12() method
    """
    assert (
        x12_mock_model.x12()
        == "MCK*JOHN*DOE*1400 ANYHOO LANE^PLEASANTVILLE^SC^90210*19800101*070500~"
    )

    x12_mock_model.birth_date = None
    assert (
        x12_mock_model.x12()
        == "MCK*JOHN*DOE*1400 ANYHOO LANE^PLEASANTVILLE^SC^90210**070500~"
    )

    x12_mock_model.address = None
    assert x12_mock_model.x12() == "MCK*JOHN*DOE***070500~"

    x12_mock_model.creation_time = None
    assert x12_mock_model.x12() == "MCK*JOHN*DOE~"


def test_x12_delimiter_defaults(x12_delimiters):
    assert x12_delimiters.component_separator == ":"
    assert x12_delimiters.element_separator == "*"
    assert x12_delimiters.repetition_separator == "^"
    assert x12_delimiters.segment_terminator == "~"


def test_x12_loop_model(x12_mock_loop):
    assert (
        x12_mock_loop.x12() == "ST*270*0001*005010X279A1~\nNM1*PR*2*ACME*****PI*12345~"
    )
