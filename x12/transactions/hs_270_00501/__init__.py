from typing import List

from pydantic import BaseModel

from x12.segments import BhtSegment, SeSegment, StSegment

from .loops import Loop2000A

"""
batch mode = multiple patients
real time = single patient
HEADER
2000A
2000B
2000C
2000D


"""


class EligibilityInquiry(BaseModel):
    """
    The Eligibility/270 transaction
    """
    st_segment: StSegment
    bht_segment: BhtSegment
    loop_2000a: List[Loop2000A]
    se_segment: SeSegment
