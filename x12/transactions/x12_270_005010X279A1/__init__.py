from pydantic import BaseModel

from x12.transactions.x12_270_005010X279A1.loops import Header, Loop2000A

"""
batch mode = multiple patients
real time = single patient
HEADER
2000A
2000B
2000C
2000D
FOOTER


"""


class EligibilityInquiry(BaseModel):
    """
    The Eligibility/270 transaction
    """

    header: Header
    loop_2000A: Loop2000A

    pass
