"""
loops.py

Models the loops, or logical segment groupings, for the Eligibility 270 5010 transaction set.

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

"""

from x12.models import X12SegmentGroup
from x12.segments import SeSegment
from x12.transactions.x12_270_005010X279A1.segments import (
    HeaderBhtSegment,
    HeaderStSegment,
    Loop2000AHlSegment,
    Loop2100ANm1Segment,
)


class Header(X12SegmentGroup):
    """
    Transaction Header Information
    """

    st_segment: HeaderStSegment
    bht_segment: HeaderBhtSegment


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


class Footer(X12SegmentGroup):
    """
    Transaction Footer Information
    """

    se_segment: SeSegment
