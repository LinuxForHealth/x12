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
    SeSegment, ActSegment
)
from .segments import (
    HeaderStSegment,
    HeaderRefSegment,
    HeaderDtpSegment,
    HeaderQtySegment,
    Loop1000AN1Segment,
    Loop1000BN1Segment,
    Loop1000CN1Segment,
)
from typing import List, Optional
from pydantic import Field
from linuxforhealth.x12.v5010.segments import BgnSegment


class Header(X12SegmentGroup):
    """
    Transaction Header Information
    """

    st_segment: HeaderStSegment
    bgn_segment: BgnSegment
    ref_segment: Optional[HeaderRefSegment]
    dtp_segment: Optional[List[HeaderDtpSegment]] = Field(max_items=6)
    qty_segment: Optional[List[HeaderQtySegment]] = Field(max_items=3)


class Loop1000A(X12SegmentGroup):
    """
    Sponsor Name
    """

    n1_segment: Loop1000AN1Segment


class Loop1000B(X12SegmentGroup):
    """
    Payer
    """

    n1_segment: Loop1000BN1Segment


class Loop1100C(X12SegmentGroup):
    """
    TPA/Broker Account Information
    """

    act_segment: ActSegment


class Loop1000C(X12SegmentGroup):
    """
    TPA/Broker Name
    """

    n1_segment: Loop1000CN1Segment
    loop_1100c: Optional[Loop1100C]


class Footer(X12SegmentGroup):
    """
    Transaction Footer Information
    """

    se_segment: SeSegment
