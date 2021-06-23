from x12.transactions import get_transaction_model
from x12.transactions.x12_270_005010X279A1 import EligibilityInquiry
from x12.transactions.x12_271_005010X279A1 import EligibilityInformation


def test_get_transaction_model():
    transaction_model = get_transaction_model("270", "005010X279A1")
    assert EligibilityInquiry.__class__ == transaction_model.__class__

    transaction_model = get_transaction_model("271", "005010X279A1")
    assert EligibilityInformation.__class__ == transaction_model.__class__
