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

from typing import Literal

from x12.models import X12BaseSegmentGroup
from x12.segments import SeSegment
from x12.transactions.x12_270_005010X279A1.segments import (
    HeaderBhtSegment,
    HeaderStSegment,
    Loop2000AHlSegment,
    Loop2100ANm1Segment,
)


class Header(X12BaseSegmentGroup):
    """
    Transaction Header Information
    """

    name: Literal["HEADER"]
    description: Literal["270 Transaction Set Header"]
    st_segment: HeaderStSegment
    bht_segment: HeaderBhtSegment


class Loop2100A(X12BaseSegmentGroup):
    """
    Loop 2100A - Information Source Name
    """

    name: Literal["Loop2100A"]
    description: Literal["Information Source Name"]
    nm1_segment: Loop2100ANm1Segment


class Loop2000A(X12BaseSegmentGroup):
    """
    Loop 2000A - Information Source
    The root node/loop for the 270 transaction

    """

    name: Literal["Loop2000A"]
    description: Literal["Information Source"]
    hl_segment: Loop2000AHlSegment
    loop_2100a: Loop2100A


class Footer(X12BaseSegmentGroup):
    """
    Transaction Footer Information
    """

    se_segment: SeSegment
