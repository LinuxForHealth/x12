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
    N1Segment,
    N3Segment,
    N4Segment,
)
from .segments import (
    HeaderStSegment,
    HeaderTrnSegment,
    HeaderCurSegment,
    HeaderRefSegment,
    Loop1000ARefSegment,
    Loop1000APerSegment,
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

    n1_segment: N1Segment
    n3_segment: N3Segment
    n4_segment: N4Segment
    ref_segment: Optional[List[Loop1000ARefSegment]] = Field(min_items=0, max_items=4)
    per_segment: Optional[List[Loop1000APerSegment]]


class Footer(X12SegmentGroup):
    """
    Transaction Footer Information
    """

    se_segment: SeSegment
