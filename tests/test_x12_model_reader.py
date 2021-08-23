"""
test_x12_model_reader.py

Supports general model streaming tests validating the number of models returned, expected payload, etc.
"""
from x12.io import X12ModelReader


def test_multiple_transactions(
    x12_control_header, x12_control_footer, x12_270_subscriber_transaction
):
    transactions: str = x12_270_subscriber_transaction * 2
    x12_input = f"{x12_control_header}{transactions}{x12_control_footer}"

    with X12ModelReader(x12_input) as r:
        model_result = [m for m in r.models()]
        assert len(model_result) == 2
        assert model_result[0].x12() == x12_270_subscriber_transaction


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
