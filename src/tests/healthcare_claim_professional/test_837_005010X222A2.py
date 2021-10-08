"""
test_837_005010XX222A2.py
"""
from x12.io import X12ModelReader


def test_837_commercial_insurance_dependent(
    x12_837_commercial_insurance_dependent_input,
    x12_837_commercial_insurance_dependent_transaction,
):
    """
    Tests specification example #1: Commercial Health Insurance (dependent transaction)
    Patient is a different person than the Subscriber.
    Payer is commercial health insurance company.

    :param x12_837_commercial_insurance_dependent_input: The full X12 control envelope.
    :param x12_837_commercial_insurance_dependent_transaction: The 837 transaction set.
    """
    with X12ModelReader(x12_837_commercial_insurance_dependent_input) as r:
        model_result = [m for m in r.models()]
        assert len(model_result) == 1
        assert (
            model_result[0].x12() == x12_837_commercial_insurance_dependent_transaction
        )


def test_837_commercial_insurance_subscriber(
    x12_837_commercial_insurance_subscriber_input,
    x12_837_commercial_insurance_subscriber_transaction,
):
    """
    Tests a subscriber transactions based on example #1: Commercial Health Insurance
    Patient is the Subscriber.
    Payer is commercial health insurance company.

    :param x12_837_commercial_insurance_subscriber_input: The full X12 control envelope.
    :param x12_837_commercial_insurance_subscriber_transaction: The 837 transaction set.
    """
    with X12ModelReader(x12_837_commercial_insurance_subscriber_input) as r:
        model_result = [m for m in r.models()]
        assert len(model_result) == 1
        assert (
            model_result[0].x12() == x12_837_commercial_insurance_subscriber_transaction
        )
