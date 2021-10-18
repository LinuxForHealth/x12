"""
assert.py

Reusable assertions for X12 based test cases
"""
from x12.io import X12ModelReader


def assert_eq_model(x12_input: str):
    """
    Asserts that a generated X12 model is equal to provided input.

    :param x12_input: The X12 input
    """

    with X12ModelReader(x12_input) as r:
        segment_terminator = r._x12_segment_reader.delimiters.segment_terminator
        segments = x12_input.split("~")

        assert segments[0].startswith("ISA")
        assert segments[1].startswith("GS")
        assert segments[-2].startswith("GE")
        assert segments[-1].startswith("IEA")


