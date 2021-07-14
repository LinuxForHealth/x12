"""
test_parsing.py

Tests the X12 base parse module
"""
import pytest
from x12.parsing import create_parser
from x12.transactions.x12_270_005010X279A1.parsing import EligibilityInquiryParser
from x12.models import X12Delimiters


def test_load_parser():
    """
    Tests the parser load process and validates the segment_parser dictionary which contains parsing functions.
    """

    parser = create_parser("270", "005010X279A1", X12Delimiters())
    assert isinstance(parser, EligibilityInquiryParser)
    assert len(EligibilityInquiryParser.loop_parsers) > 1
    assert "ST" in EligibilityInquiryParser.loop_parsers
    assert "SE" in EligibilityInquiryParser.loop_parsers

    with pytest.raises(ModuleNotFoundError):
        create_parser("911", "bad-bad-version", X12Delimiters())
