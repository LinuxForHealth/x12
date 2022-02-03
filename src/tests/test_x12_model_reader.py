"""
test_x12_model_reader.py

Supports general model streaming tests validating the number of models returned, expected payload, etc.
"""
from linuxforhealth.x12.io import X12ModelReader
from linuxforhealth.x12.models import X12Delimiters, X12SegmentGroup
from typing import Dict, List
import pytest


def test_multiple_transactions(large_x12_message):

    with X12ModelReader(large_x12_message) as r:
        model_result = [m for m in r.models()]
        assert len(model_result) == 10


@pytest.mark.parametrize("output_delimiters", [True, False])
def test_custom_delimiters(x12_with_custom_delimiters, output_delimiters):
    """
    Validates that custom delimiters are parsed correctly and generate expected x12

    :param x12_with_custom_delimiters: The X12 sample transaction
    :param output_delimiters:
    """

    # remove control segments from the x12 transaction with custom delimiters
    control_segments = ("ISA", "GS", "GE", "IEA")
    expected_segments = []
    x12_delimiters = X12Delimiters(element_separator="|", segment_terminator="?")

    for x in x12_with_custom_delimiters.split("\n"):
        if x.split("|")[0] in control_segments:
            continue
        expected_segments.append(x)

    expected_transaction = "\n".join(expected_segments)

    with X12ModelReader(
        x12_with_custom_delimiters, output_delimiters=output_delimiters
    ) as r:
        model_result = [m for m in r.models()]
        assert len(model_result) == 1
        model = model_result[0]
        assert model.x12(custom_delimiters=x12_delimiters) == expected_transaction

    # validate custom delimiter handling based on the output_delimiters flag
    st_segment = model.header.st_segment
    if output_delimiters:
        assert st_segment.delimiters.element_separator == "|"
        assert st_segment.delimiters.repetition_separator == "^"
        assert st_segment.delimiters.component_separator == ":"
        assert st_segment.delimiters.segment_terminator == "?"
    else:
        assert st_segment.delimiters is None


def _assert_delimiters(data: Dict, delimiters_exist: bool):
    """
    Parameterized helper function for test_output_delimiters.
    The function recursively examines a X12 transaction dictionary and executes
    assertions testing for the existence or absence of delimiters within a X12 segment dictionary.

    :param data: The X12 data dictionary
    :param delimiters_exist: When True assertions check for delimiter existence.
    """
    for k, v in data.items():
        if k.endswith("segment") and delimiters_exist:
            assert v["delimiters"]
        elif k.endswith("segment") and not delimiters_exist:
            assert v.get("delimiters") is None
        elif isinstance(v, dict):
            _assert_delimiters(v, delimiters_exist)


@pytest.mark.parametrize("output_delimiters", [True, False])
def test_output_delimiters(simple_270_with_new_lines, output_delimiters):
    """Tests the X12ModelReader output_delimiter flag"""
    with X12ModelReader(
        simple_270_with_new_lines, output_delimiters=output_delimiters
    ) as r:
        model_result: List[X12SegmentGroup] = [m for m in r.models()]
        assert len(model_result) == 1

        model_data = model_result[0].dict()
        _assert_delimiters(model_data, output_delimiters)
