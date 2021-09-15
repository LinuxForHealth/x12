"""
transaction_set.py

Defines the Professional Claims 837 005010X222A2 transaction set model.
"""

from x12.models import X12SegmentGroup
from .loops import Header, Footer, Loop1000A, Loop1000B, Loop2000A
from pydantic import Field
from typing import List


class HealthCareClaimProfessional(X12SegmentGroup):
    """
    The HealthCare Claim - Professional transaction model (837)
    """

    header: Header
    loop_1000a: Loop1000A
    loop_1000b: Loop1000B
    loop_2000a: List[Loop2000A] = Field(min_items=1)
    footer: Footer
