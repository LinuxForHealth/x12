"""
loops.py

Models the loops, or logical segment groupings, for the Eligibility 270 005010X279A1 transaction set.
The Eligibility Transaction set organizes loops into a hierarchical and nested model.

- Header
- Loop 2000A (Information Source)
    -- Loop 2100A (Information Source Name)
    -- Loop 2000B (Information Receiver)
        --- Loop 2100B (Information Receiver Name)
        --- Loop 2000C (Subscriber)
            --- Loop 2100C (Subscriber Name)
                --- Loop 2110C (Subscriber Eligibility)
            --- Loop 2000D (Dependent)
                --- Loop 2100D (Dependent Name)
                    --- Loop 2110D (Dependent Eligibility)
-- Footer

The Header and Footer components are not "loops" per the specification, but are included to standardize and simplify
transactional modeling and processing.
"""

from x12.models import X12SegmentGroup
from x12.segments import (
    SeSegment,
    N3Segment,
    N4Segment,
    PrvSegment,
    TrnSegment,
    DmgSegment,
    HiSegment,
)
from .segments import (
    HeaderStSegment,
    HeaderBhtSegment,
    Loop2000DHlSegment,
    Loop2000CHlSegment,
    Loop2100BNm1Segment,
    Loop2000BHlSegment,
    Loop2100BRefSegment,
    Loop2100ANm1Segment,
    Loop2000AHlSegment,
    Loop2100CNm1Segment,
    Loop2100CRefSegment,
    Loop2100CInsSegment,
    Loop2100CDtpSegment,
    Loop2110CEqSegment,
    Loop2110CAmtSegment,
    Loop2110CIiiSegment,
    Loop2110CRefSegment,
    Loop2110CDtpSegment,
)
from typing import List, Optional
from pydantic import Field


class Header(X12SegmentGroup):
    """
    Transaction Header Information
    """

    st_segment: HeaderStSegment
    bht_segment: HeaderBhtSegment


class Loop2000D(X12SegmentGroup):
    """
    Loop 2000D - Dependent
    """

    hl_segment: Loop2000DHlSegment


class Loop2110C(X12SegmentGroup):
    """
    Loop2110C - Subscriber Eligibility
    """

    eq_segment: Optional[Loop2110CEqSegment]
    amt_segment: Optional[List[Loop2110CAmtSegment]] = Field(min_items=0, max_items=2)
    iii_segment: Optional[Loop2110CIiiSegment]
    ref_segment: Optional[Loop2110CRefSegment]
    dtp_segment: Optional[Loop2110CDtpSegment]


class Loop2100C(X12SegmentGroup):
    """
    Loop 2100C - Subscriber Name
    """

    nm1_segment: Loop2100CNm1Segment
    ref_segment: Optional[List[Loop2100CRefSegment]] = Field(min_items=0, max_items=9)
    n3_segment: Optional[N3Segment]
    n4_segment: Optional[N4Segment]
    prv_segment: Optional[PrvSegment]
    dmg_segment: Optional[DmgSegment]
    ins_segment: Optional[Loop2100CInsSegment]
    hi_segment: Optional[HiSegment]
    dtp_segment: Optional[Loop2100CDtpSegment]
    loop_2110c: Loop2110C


class Loop2000C(X12SegmentGroup):
    """
    Loop 2000C - Subscriber
    """

    hl_segment: Loop2000CHlSegment
    trn_segment: Optional[List[TrnSegment]] = Field(min_items=0, max_items=2)
    loop_2100c: Loop2100C
    loop_2000d: Optional[List[Loop2000D]] = Field(min_items=0)


class Loop2100B(X12SegmentGroup):
    """
    Loop 2100B - Information Receiver Name
    """

    nm1_segment: Loop2100BNm1Segment
    ref_segment: Optional[List[Loop2100BRefSegment]]
    n3_segment: Optional[N3Segment]
    n4_segment: Optional[N4Segment]
    prv_segment: Optional[PrvSegment]


class Loop2000B(X12SegmentGroup):
    """
    Loop 2000B - Information Receiver
    """

    hl_segment: Loop2000BHlSegment
    loop_2100b: Loop2100B
    loop_2000c: List[Loop2000C] = Field(min_items=1)


class Loop2100A(X12SegmentGroup):
    """
    Loop 2100A - Information Source Name
    """

    nm1_segment: Loop2100ANm1Segment


class Loop2000A(X12SegmentGroup):
    """
    Loop 2000A - Information Source
    The root node/loop for the 270 transaction

    """

    hl_segment: Loop2000AHlSegment
    loop_2100a: Loop2100A
    loop_2000b: List[Loop2000B] = Field(min_items=1)


class Footer(X12SegmentGroup):
    """
    Transaction Footer Information
    """

    se_segment: SeSegment
