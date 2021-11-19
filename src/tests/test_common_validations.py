"""
test_common_validations.py

Tests common validations that are shared across X12 transaction sets.
"""
from linuxforhealth.x12.io import X12ModelReader
import pytest


def test_segment_footer_count(simple_270_with_new_lines):
    """Validates the total segment count validation raises an exception"""
    test_input = simple_270_with_new_lines.replace("SE*17*0001~", "SE*27*0001~")
    with pytest.raises(ValueError):
        with X12ModelReader(test_input) as r:
            for _ in r.models():
                pass
