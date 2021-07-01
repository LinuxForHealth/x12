"""
transaction_set.py

Defines the Eligibility 270 005010X279A1 transaction set model.
"""

from typing import List

from x12.models import X12SegmentGroup

from .loops import Footer, Header, Loop2000A


class EligibilityInquiry(X12SegmentGroup):
    """ """

    header: Header
    loop_2000a: List[Loop2000A]
    footer: Footer
