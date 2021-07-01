"""
test_parsing.py

Tests the X12 base parse module
"""
import pytest

from x12.parsing import X12SegmentParser
from x12.transactions.x12_270_005010X279A1.parse import EligibilityInquiryParser


def test_load_parser():
    parser = X12SegmentParser.load_parser("270", "005010X279A1")
    assert isinstance(parser, EligibilityInquiryParser)

    with pytest.raises(ModuleNotFoundError):
        X12SegmentParser.load_parser("911", "bad-bad-version")
