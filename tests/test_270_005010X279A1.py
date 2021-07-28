"""
Tests use-cases for the 005010X279A1 (Eligibility Inquiry and Response) transactions
"""

from x12.io import X12ModelReader


def test_270_subscriber(x12_270_subscriber_input, x12_270_subscriber_transaction):
    with X12ModelReader(x12_270_subscriber_input) as r:
        model_result = [m for m in r.models()]
        assert len(model_result) == 1
        assert model_result[0].x12() == x12_270_subscriber_transaction


def test_270_dependent(x12_270_dependent_input, x12_270_dependent_transaction):
    with X12ModelReader(x12_270_dependent_input) as r:
        model_result = [m for m in r.models()]
        assert len(model_result) == 1
        assert model_result[0].x12() == x12_270_dependent_transaction
