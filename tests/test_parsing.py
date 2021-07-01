"""
test_parsing.py

Tests the X12 base parse module
"""
import pytest
from typing import Dict
from x12.parsing import X12SegmentParser, match
from x12.transactions.x12_270_005010X279A1.parsing import EligibilityInquiryParser


@pytest.fixture
def segment_data(x12_delimiters) -> Dict[str, str]:
    """
    The segment_data fixture represents a "parsed" segment from a X12 stream.
    Streams are list of values which are "parsed" into a dictionary with field names.
    """
    return {
        "delimiters": x12_delimiters.dict(),
        "segment_name": "ST",
        "transaction_set_identifier_code": "270",
        "transaction_set_control_number": "0001",
        "implementation_convention_reference": "005010X279A1",
    }


@pytest.fixture
def data_context():
    """
    The data_context fixture is a stub or placeholder for the parsing function.
    """
    return {}


@pytest.fixture
def data_record():
    """
    The data_record fixture is the parsing "target" for the parsing function.
    """
    return {"header": {"st_segment": None}}


@pytest.fixture
def mock_parsing_function():
    """
    The mock parsing fixture is a function which will parse segment_data into a data_record.
    """

    def parse_st_segment(segment_data, data_context, data_record):
        data_record["header"]["st_segment"] = segment_data

    return parse_st_segment


def test_match_no_conditions(
    mock_parsing_function, segment_data, data_context, data_record
):
    """
    Tests the match decorator when no conditions are specified.
    """
    wrapped_func = match("ST")(mock_parsing_function)
    wrapped_func(segment_data, data_context, data_record)
    assert data_record["header"]["st_segment"] == segment_data


def test_match_conditions(
    mock_parsing_function, segment_data, data_context, data_record
):
    """
    Tests the match decorator when conditions are specified.
    """
    wrapped_func = match("ST", conditions={"transaction_set_identifier_code": "270"})(
        mock_parsing_function
    )
    wrapped_func(segment_data, data_context, data_record)
    assert data_record["header"]["st_segment"] == segment_data


def test_match_conditions_unmatched(
    mock_parsing_function, segment_data, data_context, data_record
):
    """
    Tests the match decorator when conditions are specified but they do not match the data_segment.
    """
    wrapped_func = match("ST", conditions={"transaction_set_identifier_code": "911"})(
        mock_parsing_function
    )
    wrapped_func(segment_data, data_context, data_record)
    assert data_record["header"]["st_segment"] is None


def test_load_parser():
    """
    Tests the parser load process and validates the segment_parser dictionary which contains parsing functions.
    """
    parser = X12SegmentParser.load_parser("270", "005010X279A1")
    assert isinstance(parser, EligibilityInquiryParser)
    assert len(EligibilityInquiryParser.segment_parsers) > 1
    assert "ST" in EligibilityInquiryParser.segment_parsers
    assert "SE" in EligibilityInquiryParser.segment_parsers

    with pytest.raises(ModuleNotFoundError):
        X12SegmentParser.load_parser("911", "bad-bad-version")
