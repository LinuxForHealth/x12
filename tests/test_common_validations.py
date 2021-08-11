"""
test_common_validations.py

Tests common validations that are shared across X12 transaction sets.
"""
from x12.io import X12ModelReader
import pytest


def test_segment_footer_count(x12_270_subscriber_input):
    """Validates the total segment count validation raises an exception"""
    test_input = x12_270_subscriber_input.replace("SE*27*0001~", "SE*17*0001~")
    with pytest.raises(ValueError):
        with X12ModelReader(test_input) as r:
            for _ in r.models():
                pass
