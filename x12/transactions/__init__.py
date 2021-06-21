"""
transactions package
"""
from x12.transactions import hs_270_00501, hb_271_00501

# maps x12.models.X12VersionIdentifier string to a transaction model
transaction_map = {
    "00501_hs_270_005010X279A1": hs_270_00501.EligibilityInquiry,
    "00501_hb_270_005010X279A1": hb_271_00501.EligibilityInformation,
}
