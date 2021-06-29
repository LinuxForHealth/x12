from x12.models import X12SegmentGroup
from .loops import Header, Footer, Loop2000A
from typing import List

"""
"""


class EligibilityInquiry(X12SegmentGroup):
    """ """

    header: Header
    loop_2000A: List[Loop2000A]
    footer: Footer
