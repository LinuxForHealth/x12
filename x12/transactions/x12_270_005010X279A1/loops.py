"""
loops.py

Models the loops, or logical segment groupings, for the Eligibility 270 5010 transaction set.
LinuxForHealth X12 includes headers and footers within loops to standardize processing.

The 270 is a hierarchical structure with the Information Source, payer or clearinghouse, acting as the root.
The general loop structure for the 270 transaction includes:

    - Information Receiver (Loop 2000B)
    - - Subscriber (Loop 2000C)
    - - - Dependent (Loop 2000D)
    - - - - Eligibility/Benefit Inquiry
"""

from typing import Literal

from x12.models import X12BaseLoopModel
from x12.transactions.x12_270_005010X279A1.segments import (
    HeaderBhtSegment,
    HeaderStSegment,
    Loop2000AHlSegment,
    Loop2100ANm1Segment,
)


class Header(X12BaseLoopModel):
    """
    Transaction Header Information
    """

    loop_name: Literal["HEADER"]
    loop_description: Literal["270 Transaction Set Header"]
    st_segment: HeaderStSegment
    bht_segment: HeaderBhtSegment


class Loop2100A(X12BaseLoopModel):
    """
    Loop 2100A - Information Source Name
    """

    loop_name: Literal["Loop2100A"]
    loop_description: Literal["Information Source Name"]
    nm1_segment: Loop2100ANm1Segment


class Loop2000A(X12BaseLoopModel):
    """
    Loop 2000A - Information Source
    The root node/loop for the 270 transaction

    """

    loop_name: Literal["Loop2000A"]
    loop_description: Literal["Information Source"]
    hl_segment: Loop2000AHlSegment
    loop_2100a: Loop2100A
