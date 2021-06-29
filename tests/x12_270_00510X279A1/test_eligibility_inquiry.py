from x12.transactions.x12_270_005010X279A1 import EligibilityInquiry


def test_it():
    for f in EligibilityInquiry.__fields__.values():
        x = 1
        print(f)
