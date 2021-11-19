"""
support.py

Reusable assertions and utilities for X12 based test cases
"""
from linuxforhealth.x12.io import X12ModelReader
import os

# base resource directory for "file fixtures" (sample x12 transactions)
resources_directory = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "resources",
)


def assert_eq_model(x12_path: str):
    """
    Asserts that a generated X12 model is equal to provided input.
    `assert_eq_model` is constrained to processing an input with a single functional group, but does support
    multiple transaction sets.

    :param x12_path: The path to a X12 file
    """
    with open(x12_path) as f:
        x12_data = "".join([l for l in f.readlines() if l])

        with X12ModelReader(x12_data) as r:

            segment_terminator = r._x12_segment_reader.delimiters.segment_terminator
            segments = [
                s for s in x12_data.split(segment_terminator) if s and s != "\n"
            ]

            assert "ISA" in segments[0]
            assert "GS" in segments[1]
            assert "GE" in segments[-2]
            assert "IEA" in segments[-1]

            control_header = (
                segment_terminator.join(segments[0:2]) + segment_terminator + "\n"
            )
            control_footer = segment_terminator.join(segments[-2:]) + segment_terminator
            transaction_sets: str = ""

            for m in r.models():
                transaction_sets += m.x12()

            actual = f"{control_header}{transaction_sets}{control_footer}"
            assert actual == x12_data
