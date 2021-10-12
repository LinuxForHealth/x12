"""
test_835_005010XX221A1.py
"""
from x12.io import X12ModelReader


def test_835_managed_care(
    x12_835_managed_care_input,
    x12_835_managed_care_transaction,
):
    """
    Tests specification example #2: 835 usage in a managed care environment.
    Within the managed care environment, dollars and data are sent separately.

    :param x12_835_managed_care_input: The full X12 control envelope.
    :param x12_835_managed_care_transaction: The 837 transaction set.
    """
    with X12ModelReader(x12_835_managed_care_input) as r:
        model_result = [m for m in r.models()]
        assert len(model_result) == 1
        assert model_result[0].x12() == x12_835_managed_care_transaction
