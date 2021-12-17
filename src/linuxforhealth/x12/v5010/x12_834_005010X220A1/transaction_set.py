"""
transaction_set.py

Defines the Enrollment 834 005010X220A1 transaction set model.
"""

from typing import List, Optional

from linuxforhealth.x12.models import X12SegmentGroup

from .loops import Footer, Header, Loop1000A, Loop1000B, Loop1000C, Loop2000
from pydantic import root_validator, Field
from linuxforhealth.x12.validators import validate_segment_count


class BenefitEnrollmentAndMaintenance(X12SegmentGroup):
    """
    The ASC X12 834 (Benefit Enrollment and Maintenance) transaction model.
    """

    header: Header
    loop_1000a: Loop1000A
    loop_1000b: Loop1000B
    loop_1000c: Optional[List[Loop1000C]] = Field(max_items=2)
    loop_2000: List[Loop2000]
    footer: Footer

    _validate_segment_count = root_validator(allow_reuse=True)(validate_segment_count)
