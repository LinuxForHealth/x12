"""
loops.py

Models the loops, or logical segment groupings, for the Health Care Claim Status Request 276 005010X212 transaction set.
The Health Care Claim Status Request organizes loops into a hierarchical and nested model.

-- Header
    -- Loop 2000A (Information Source)
        -- Loop 2100A (Payer Name)
        -- Loop 2000B (Information Receiver)
            -- Loop 2100B (Information Receiver Name)
            -- Loop 2000C (Service Provider Detail)
                -- Loop 2100C (Provider Name)
                -- Loop 2000D (Subscriber Level)
                    -- Loop 2100D (Subscriber Name)
                    -- Loop 2200D (Claim Status Tracking Number)
                        -- Loop 2210D (Service Line Information)
                    -- Loop 2000E (Dependent Level)
                        -- Loop 2100E (Dependent Name)
                        -- Loop 2200E (Claim Status Tracking Number)
                            -- Loop 2210E (Service Line Information)
-- Footer
"""
from x12.models import X12SegmentGroup
from .segments import (
    HeaderStSegment,
    HeaderBhtSegment,
    Loop2000AHlSegment,
    Loop2100ANm1Segment,
    Loop2000BHlSegment,
    Loop2100BNm1Segment,
)
from x12.segments import SeSegment
from typing import List
from pydantic import Field


class Header(X12SegmentGroup):
    """
    Transaction Header Information
    """

    st_segment: HeaderStSegment
    bht_segment: HeaderBhtSegment


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


class Loop2100A(X12SegmentGroup):
    """
    Loop 2100A - Payer Name
    """

    nm1_segment: Loop2100ANm1Segment


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
