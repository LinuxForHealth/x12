"""
transaction_set.py

Defines the Professional Claims 837 005010X222A2 transaction set model.
"""

from linuxforhealth.x12.models import X12SegmentGroup
from .loops import Header, Footer, Loop1000A, Loop1000B, Loop2000A
from pydantic import Field, root_validator
from typing import List
from linuxforhealth.x12.validators import validate_segment_count


class HealthCareClaimProfessional(X12SegmentGroup):
    """
    The HealthCare Claim - Professional transaction model (837)
    """

    header: Header
    loop_1000a: Loop1000A
    loop_1000b: Loop1000B
    loop_2000a: List[Loop2000A] = Field(min_items=1)
    footer: Footer

    _validate_segment_count = root_validator(allow_reuse=True)(validate_segment_count)
