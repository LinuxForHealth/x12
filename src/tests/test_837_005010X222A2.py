"""
test_837_005010XX222A2.py
"""
from x12.io import X12ModelReader


def test_837_commercial_health_insurance(
    x12_837_commercial_health_insurance_input,
    x12_837_commercial_health_insurance_transaction,
):
    """
    Tests specification example #1: Commercial Health Insurance.
    Patient is a different person than the Subscriber.
    Payer is commercial health insurance company.

    :param x12_837_commercial_health_insurance_input: The full X12 control envelope.
    :param x12_837_commercial_health_insurance_transaction: The 837 transaction set.
    """
    with X12ModelReader(x12_837_commercial_health_insurance_input) as r:
        model_result = [m for m in r.models()]
        assert len(model_result) == 1
        assert model_result[0].x12() == x12_837_commercial_health_insurance_transaction
