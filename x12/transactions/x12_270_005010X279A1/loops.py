"""
loops.py

Models the loops, or logical segment groupings, for the Eligibility 270 5010 transaction set.

- Header
- Loop 2000A (Information Source) - HL*1**20*1
    -- Loop 2100A (Information Source Name) - NM1*PR*etc*etc~
    -- Loop 2000B (Information Receiver) - HL*2**21*1
        --- Loop 2100B (Information Receiver Name) - NM1*1P*etc*etc
        --- Loop 2000C (Subscriber) - HL*3*2*22*1~
            --- Loop 2100C (Subscriber Name) - NM*1*etc~
                --- Loop 2110C (Subscriber Eligibility) - EQ*etc~
            --- Loop 2000D (Dependent) - HL*4*3*23*0~
                --- Loop 2100D (Dependent Name) - NM1*03*etc~
                    --- Loop 2110D (Dependent Eligibility) EQ*etc~
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
