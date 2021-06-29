"""
test_parsing.py

Test cases for the match decorator used to parse X12 segments into a "data record" (Dictionary) structure.
"""
import pytest
from typing import List, Dict, Callable
from x12.parsing import match


@pytest.fixture
def st_segment() -> List[str]:
    """Returns a tokenized ST segment fixture"""
    return ["ST", "270", "0001", "005010X279A1"]


@pytest.fixture
def ge_segment() -> List[str]:
    """Returns a tokenized GE segment fixture"""
    return ["GE", "1", "1"]


@pytest.fixture
def data_record() -> Dict[str, str]:
    """Initializes an empty data record/dictionary"""
    return {}


@pytest.fixture
def parsed_st_segment() -> Dict[str, Dict[str, str]]:
    """Returns a parsed ST segment representation"""
    return {
        "header": {
            "transaction_set_identifier_code": "270",
            "transaction_set_control_number": "0001",
            "implementation_convention_reference": "005010X279A1"
        }
    }


@pytest.fixture
def mock_func_no_conditions() -> Callable:
    """Returns a mock function configured to match on ST segments"""
    @match("ST")
    def mock_function_a(segment_data, data_context, data_record):
        data_record["header"] = {
            "transaction_set_identifier_code": segment_data[1],
            "transaction_set_control_number": segment_data[2],
            "implementation_convention_reference": segment_data[3]
        }
    return mock_function_a


@pytest.fixture
def mock_func_with_conditions() -> Callable:
    """Returns a mock function configured to match on ST segments with two field conditions"""
    @match("ST", {1: "270", 2: "0001"})
    def mock_function_b(segment_data, data_context, data_record):
        data_record["header"] = {
            "transaction_set_identifier_code": segment_data[1],
            "transaction_set_control_number": segment_data[2],
            "implementation_convention_reference": segment_data[3]
        }
    return mock_function_b


def test_match_no_conditions(mock_func_no_conditions, st_segment, data_record, parsed_st_segment):
    mock_func_no_conditions(st_segment, {}, data_record)
    assert data_record == parsed_st_segment
    assert mock_func_no_conditions.segment_group == "ST"


def test_match_no_match(mock_func_no_conditions, ge_segment, data_record):
    mock_func_no_conditions(ge_segment, {}, data_record)
    assert data_record == {}


def test_match_with_conditions(mock_func_with_conditions, st_segment, data_record, parsed_st_segment):
    mock_func_with_conditions(st_segment, {}, data_record)
    assert data_record == parsed_st_segment
    assert mock_func_with_conditions.segment_group == "ST"
