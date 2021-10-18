"""
support.py

Reusable assertions and utilities for X12 based test cases
"""
from x12.io import X12ModelReader


def assert_eq_model(x12_input: str):
    """
    Asserts that a generated X12 model is equal to provided input.
    `assert_eq_model` is constrained to processing an input with a single functional group, but does support
    multiple transaction sets.

    :param x12_input: The X12 input
    """
    one_line_input = x12_input.replace("\n", "")

    with X12ModelReader(one_line_input) as r:
        segment_terminator = r._x12_segment_reader.delimiters.segment_terminator
        segments = one_line_input.split(segment_terminator)
        segments = [s for s in segments if s]

        assert segments[0].startswith("ISA")
        assert segments[1].startswith("GS")
        assert segments[-2].startswith("GE")
        assert segments[-1].startswith("IEA")

        control_header = segment_terminator.join(segments[0:2]) + segment_terminator
        control_footer = segment_terminator.join(segments[-2:]) + segment_terminator
        transaction_sets: str = ""

        for m in r.models():
            transaction_sets += m.x12(use_new_lines=False)

        actual = f"{control_header}{transaction_sets}{control_footer}"
        assert actual == one_line_input
