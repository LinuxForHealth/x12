"""
loops.py

Models the loops, or logical segment groupings, for the Health Care Claim Payment 835 005010X221A1 transaction set model.
The Health Care Claim Payment transaction set organizes loops into a hierarchical and nested model.
"""
from x12.models import X12SegmentGroup
from x12.segments import (
    SeSegment,
    BprSegment,
    DtmSegment,
    N3Segment,
    N4Segment,
    RdmSegment,
    LxSegment,
    Ts3Segment,
    Ts2Segment,
)
from .segments import (
    HeaderStSegment,
    HeaderTrnSegment,
    HeaderCurSegment,
    HeaderRefSegment,
    Loop1000AN1Segment,
    Loop1000ARefSegment,
    Loop1000APerSegment,
    Loop1000BN1Segment,
    Loop1000BRefSegment,
)
from typing import Optional, List
from pydantic import Field


class Header(X12SegmentGroup):
    """
    Transaction Header Information
    """

    st_segment: HeaderStSegment
    bpr_segment: BprSegment
    trn_segment: HeaderTrnSegment
    cur_segment: Optional[HeaderCurSegment]
    ref_segment: Optional[List[HeaderRefSegment]] = Field(min_items=0, max_items=2)
    dtm_segment: Optional[DtmSegment]


class Loop1000A(X12SegmentGroup):
    """
    Loop 1000A - Payer Identification
    """

    n1_segment: Loop1000AN1Segment
    n3_segment: N3Segment
    n4_segment: N4Segment
    ref_segment: Optional[List[Loop1000ARefSegment]] = Field(min_items=0, max_items=4)
    per_segment: Optional[List[Loop1000APerSegment]]


class Loop1000B(X12SegmentGroup):
    """
    Loop 1000B - Payee Identification
    """

    n1_segment: Loop1000BN1Segment
    n3_segment: Optional[N3Segment]
    n4_segment: Optional[N4Segment]
    ref_segment: Optional[List[Loop1000BRefSegment]]
    rdm_segment: Optional[RdmSegment]


class Loop2100(X12SegmentGroup):
    """
    Loop 2100 - Claim Payment Information
    """

    pass


class Loop2000(X12SegmentGroup):
    """
    Loop 2000 - Claim Payment Header Number
    """

    lx_segment: LxSegment
    ts3_segment: Optional[Ts3Segment]
    ts2_segment: Optional[Ts2Segment]
    # loop_2100: List[Loop2100]


class Footer(X12SegmentGroup):
    """
    Transaction Footer Information
    """

    se_segment: SeSegment
