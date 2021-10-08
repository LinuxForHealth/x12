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


def test_837_subscriber_properties(x12_837_commercial_insurance_subscriber_input):
    """
    Test 837 properties where the patient is the subscriber
    """
    with X12ModelReader(x12_837_commercial_insurance_subscriber_input) as r:
        model_result = [m for m in r.models()]
        assert len(model_result) == 1

        model = model_result[0]

        nm1_segment = model.patient["loop_2010ba"]["nm1_segment"]
        assert nm1_segment["name_last_or_organization_name"] == "SMITH"
        assert nm1_segment["name_first"] == "JANE"

        claim_data = model.claim
        assert claim_data["clm_segment"] is not None
        assert len(claim_data["sv1_segment"]) == 4


def test_837_dependent_properties(x12_837_commercial_insurance_dependent_input):
    """
    Test 837 properties where the patient is the subscriber
    """
    with X12ModelReader(x12_837_commercial_insurance_dependent_input) as r:
        model_result = [m for m in r.models()]
        assert len(model_result) == 1

        model = model_result[0]
        assert "loop_2300" not in model

        nm1_segment = model.patient["loop_2010ca"]["nm1_segment"]
        assert nm1_segment["name_last_or_organization_name"] == "SMITH"
        assert nm1_segment["name_first"] == "TED"

        claim_data = model.claim
        assert claim_data["clm_segment"] is not None
        assert len(claim_data["sv1_segment"]) == 4
