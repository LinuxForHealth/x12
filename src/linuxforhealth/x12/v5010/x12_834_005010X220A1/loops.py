"""
loops.py

Models the loops, or logical segment groupings, for the Enrollment 834 005010X220A1 transaction set.

- Header
- Loop 1000A (Sponsor Name)
- Loop 1000B (Payer Name)
- Loop 1000C (TPA Broker Name)
    - Loop 1100C (TPA Broker Account Information)
- Loop 2000 (Member Level Detail)
    - Loop 2100A (Member Name)
    - Loop 2100B (Incorrect Member Name)
    - Loop 2100C (Member Mailing Address)
    - Loop 2100D (Member Employer)
    - Loop 2100E (Member School)
    - Loop 2100F (Custodial Parent)
    - Loop 2100G (Responsible Person)
    - Loop 2100H (Drop Off Location)
    - Loop 2200 (Disability Information)
    - Loop 2300 (Health Coverage)
        - Loop 2310 (Provider Information)
        - Loop 2320 (Coordination Of Benefits)
            - Loop 2330 (Coordination of Benefits Related Entity)
    - Loop 2700 (Member Reporting Categories)
        - Loop 2750 (Reporting Category)
- Footer

The Header and Footer components are not "loops" per the specification, but are included to standardize and simplify
transactional modeling and processing.
"""

from linuxforhealth.x12.models import X12SegmentGroup
from linuxforhealth.x12.v5010.segments import (
    SeSegment,
)
from .segments import (
    HeaderStSegment, HeaderRefSegment, HeaderDtpSegment, HeaderQtySegment
)
from typing import List, Optional
from pydantic import Field, root_validator
from linuxforhealth.x12.v5010.segments import BgnSegment
from linuxforhealth.x12.validators import validate_duplicate_ref_codes


class Header(X12SegmentGroup):
    """
    Transaction Header Information
    """

    st_segment: HeaderStSegment
    bgn_segment: BgnSegment
    ref_segment: HeaderRefSegment
    dtp_segment: Optional[List[HeaderDtpSegment]] = Field(max_items=6)
    qty_segment: Optional[List[HeaderQtySegment]] = Field(max_items=3)


class Footer(X12SegmentGroup):
    """
    Transaction Footer Information
    """

    se_segment: SeSegment
