"""
loops.py

Models the loops, or logical segment groupings, for the Health Care Claim Status Response 277 005010X212 transaction set.
The Health Care Claim Status Response organizes loops into a hierarchical and nested model.

-- Header
    -- Loop 2000A (Information Source)
        -- Loop 2100A (Payer Name)
        -- Loop 2000B (Information Receiver)
            -- Loop 2100B (Information Receiver Name)
            -- Loop 2200B (Information Receiver Trace Identifier)
            -- Loop 2000C (Service Provider Detail)
                -- Loop 2100C (Service Provider Name)
                -- Loop 2200C (Information Receiver Trace Identifier)
                -- Loop 2000D (Subscriber Level)
                    -- Loop 2100D (Subscriber Name)
                    -- Loop 2200D (Claim Status Tracking Number)
                        -- Loop 2220D (Service Line Information)
                    -- Loop 2000E (Dependent Level)
                        -- Loop 2100E (Dependent Name)
                        -- Loop 2200E (Claim Status Tracking Number)
                            -- Loop 2220E (Service Line Information)
-- Footer

The Subscriber and Dependent Claim Status and Service Line Loops share segment classes as the data structures
are identical.
"""
from linuxforhealth.x12.models import X12SegmentGroup
from .segments import (
    HeaderStSegment,
    HeaderBhtSegment,
    Loop2000AHlSegment,
    Loop2100ANm1Segment,
    Loop2100APerSegment,
    Loop2000BHlSegment,
    Loop2100BNm1Segment,
    Loop2200BTrnSegment,
    Loop2200CTrnSegment,
    Loop2000CHlSegment,
    Loop2100CNm1Segment,
    Loop2000DHlSegment,
    Loop2100DNm1Segment,
    Loop2200DTrnSegment,
    Loop2200DRefSegment,
    Loop2200DDtpSegment,
    Loop2220DSvcSegment,
    Loop2220DRefSegment,
    Loop2220DDtpSegment,
    Loop2000EHlSegment,
    Loop2100ENm1Segment,
)
from linuxforhealth.x12.v5010.segments import SeSegment, StcSegment
from typing import List, Optional
from pydantic import Field


class Header(X12SegmentGroup):
    """
    Transaction Header Information
    """

    st_segment: HeaderStSegment
    bht_segment: HeaderBhtSegment


class Loop2220E(X12SegmentGroup):
    """
    Dependent Claim Status Service Line Information
    The segment implementations from the Subscriber loop are used as the structure is the same.
    """

    svc_segment: Loop2220DSvcSegment
    stc_segment: List[StcSegment]
    ref_segment: Optional[Loop2220DRefSegment]
    dtp_segment: Loop2220DDtpSegment


class Loop2200E(X12SegmentGroup):
    """
    Dependent Claim Status Tracking Number
    The segment implementations from the Subscriber loop are used as the structure is the same.
    """

    trn_segment: Loop2200DTrnSegment
    stc_segment: List[StcSegment]
    ref_segment: Optional[List[Loop2200DRefSegment]] = Field(min_items=0, max_items=7)
    dtp_segment: Optional[Loop2200DDtpSegment]
    loop_2220e: Optional[List[Loop2220E]]


class Loop2100E(X12SegmentGroup):
    """
    Dependent Name
    """

    nm1_segment: Loop2100ENm1Segment


class Loop2000E(X12SegmentGroup):
    """
    Dependent Loop
    """

    hl_segment: Loop2000EHlSegment
    loop_2100e: Loop2100E
    loop_2200e: Optional[List[Loop2200E]]


class Loop2220D(X12SegmentGroup):
    """
    Subscriber Claim Status Service Line Information
    """

    svc_segment: Loop2220DSvcSegment
    stc_segment: List[StcSegment]
    ref_segment: Optional[Loop2220DRefSegment]
    dtp_segment: Loop2220DDtpSegment


class Loop2200D(X12SegmentGroup):
    """
    Subscriber Claim Status Tracking Number
    """

    trn_segment: Loop2200DTrnSegment
    stc_segment: List[StcSegment]
    ref_segment: Optional[List[Loop2200DRefSegment]] = Field(min_items=0, max_items=7)
    dtp_segment: Optional[Loop2200DDtpSegment]
    loop_2220d: Optional[List[Loop2220D]]


class Loop2100D(X12SegmentGroup):
    """
    Loop 2100D Subscriber Name
    """

    nm1_segment: Loop2100DNm1Segment


class Loop2000D(X12SegmentGroup):
    """
    Loop 2000D Subscriber
    """

    hl_segment: Loop2000DHlSegment
    loop_2100d: Loop2100D
    loop_2200d: Optional[List[Loop2200D]]
    loop_2000e: Optional[List[Loop2000E]]


class Loop2200C(X12SegmentGroup):
    """
    Loop 2200C - Service Provider Trace Trace Identifiers
    The Loop2200BTrnSegment is used as it's structure is compatible with Loop2200C
    """

    trn_segment: Loop2200CTrnSegment
    stc_segment: Optional[List[StcSegment]]


class Loop2100C(X12SegmentGroup):
    """
    Loop 2100C - Service Provider Name
    """

    nm1_segment: Loop2100CNm1Segment


class Loop2000C(X12SegmentGroup):
    """
    Loop 2000C - Service Provider
    """

    hl_segment: Loop2000CHlSegment
    loop_2100c: Loop2100C
    loop_2200c: Optional[Loop2200C]
    loop_2000d: Optional[List[Loop2000D]] = Field(min_items=1)


class Loop2200B(X12SegmentGroup):
    """
    Loop 2200B - Information Receiver Trace Identifiers
    """

    trn_segment: Loop2200BTrnSegment
    stc_segment: Optional[List[StcSegment]]


class Loop2100B(X12SegmentGroup):
    """
    Loop 2100B - Information Receiver Name
    """

    nm1_segment: Loop2100BNm1Segment


class Loop2000B(X12SegmentGroup):
    """
    Loop 2000B - Information Receiver
    """

    hl_segment: Loop2000BHlSegment
    loop_2100b: Loop2100B
    loop_2200b: Optional[Loop2200B]
    loop_2000c: Optional[List[Loop2000C]] = Field(min_items=1)


class Loop2100A(X12SegmentGroup):
    """
    Loop 2100A - Payer Name
    """

    nm1_segment: Loop2100ANm1Segment
    per_segment: Optional[Loop2100APerSegment]


class Loop2000A(X12SegmentGroup):
    """
    Loop 2000A - Information Source
    """

    hl_segment: Loop2000AHlSegment
    loop_2100a: Loop2100A
    loop_2000b: List[Loop2000B] = Field(min_items=1)


class Footer(X12SegmentGroup):
    """
    Transaction Footer Information
    """

    se_segment: SeSegment
