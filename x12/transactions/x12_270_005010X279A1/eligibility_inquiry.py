from x12.models import X12BaseSegmentGroup
from .loops import Header, Footer, Loop2000A
from typing import List

"""
"""


class EligibilityInquiry(X12BaseSegmentGroup):
    """ """

    header: Header
    loop_2000A: List[Loop2000A]
    footer: Footer
