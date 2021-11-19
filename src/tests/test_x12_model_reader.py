"""
test_x12_model_reader.py

Supports general model streaming tests validating the number of models returned, expected payload, etc.
"""
from linuxforhealth.x12.io import X12ModelReader


def test_multiple_transactions(large_x12_message):

    with X12ModelReader(large_x12_message) as r:
        model_result = [m for m in r.models()]
        assert len(model_result) == 10


def test_custom_delimiters(x12_with_custom_delimiters):

    # remove control segments from the x12 transaction with custom delimiters
    control_segments = ("ISA", "GS", "GE", "IEA")
    expected_segments = []

    for x in x12_with_custom_delimiters.split("\n"):
        if x.split("|")[0] in control_segments:
            continue
        expected_segments.append(x)

    expected_transaction = "\n".join(expected_segments)

    with X12ModelReader(x12_with_custom_delimiters) as r:
        model_result = [m for m in r.models()]
        assert len(model_result) == 1
        assert model_result[0].x12() == expected_transaction
