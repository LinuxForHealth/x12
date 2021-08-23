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
    Loop2100RefSegment,
    Loop2100CInsSegment,
    Loop2100DtpSegment,
    Loop2110EqSegment,
    Loop2110AmtSegment,
    Loop2110IiiSegment,
    Loop2110RefSegment,
    Loop2110DtpSegment,
    Loop2100DNm1Segment,
    Loop2100DInsSegment,
    Loop2100CPrvSegment,
    Loop2100BPrvSegment,
)
from typing import List, Optional
from pydantic import Field, root_validator
from x12.validators import validate_duplicate_ref_codes


class Header(X12SegmentGroup):
    """
    Transaction Header Information
    """

    st_segment: HeaderStSegment
    bht_segment: HeaderBhtSegment


class Loop2110D(X12SegmentGroup):
    """
    Loop 2110D Dependent Eligibility
    """

    eq_segment: Optional[Loop2110EqSegment]
    amt_segment: Optional[List[Loop2110AmtSegment]] = Field(min_items=0, max_items=2)
    iii_segment: Optional[Loop2110IiiSegment]
    ref_segment: Optional[Loop2110RefSegment]
    dtp_segment: Optional[Loop2110DtpSegment]


class Loop2100D(X12SegmentGroup):
    """
    Loop 2100D - Dependent Name
    """

    nm1_segment: Loop2100DNm1Segment
    ref_segment: Optional[List[Loop2100RefSegment]] = Field(min_items=0, max_items=9)
    n3_segment: Optional[N3Segment]
    n4_segment: Optional[N4Segment]
    prv_segment: Optional[Loop2100CPrvSegment]
    dmg_segment: Optional[DmgSegment]
    ins_segment: Optional[Loop2100DInsSegment]
    hi_segment: Optional[HiSegment]
    dtp_segment: Optional[Loop2100DtpSegment]
    loop_2110d: Loop2110D

    _validate_ref_segments = root_validator(allow_reuse=True)(
        validate_duplicate_ref_codes
    )


class Loop2000D(X12SegmentGroup):
    """
    Loop 2000D - Dependent
    """

    hl_segment: Loop2000DHlSegment
    trn_segment: Optional[List[TrnSegment]] = Field(min_items=0, max_items=2)
    loop_2100d: Loop2100D


class Loop2110C(X12SegmentGroup):
    """
    Loop2110C - Subscriber Eligibility
    """

    eq_segment: Optional[Loop2110EqSegment]
    amt_segment: Optional[List[Loop2110AmtSegment]] = Field(min_items=0, max_items=2)
    iii_segment: Optional[Loop2110IiiSegment]
    ref_segment: Optional[Loop2110RefSegment]
    dtp_segment: Optional[Loop2110DtpSegment]


class Loop2100C(X12SegmentGroup):
    """
    Loop 2100C - Subscriber Name
    """

    nm1_segment: Loop2100CNm1Segment
    ref_segment: Optional[List[Loop2100RefSegment]] = Field(min_items=0, max_items=9)
    n3_segment: Optional[N3Segment]
    n4_segment: Optional[N4Segment]
    prv_segment: Optional[Loop2100CPrvSegment]
    dmg_segment: Optional[DmgSegment]
    ins_segment: Optional[Loop2100CInsSegment]
    hi_segment: Optional[HiSegment]
    dtp_segment: Optional[Loop2100DtpSegment]
    loop_2110c: Optional[Loop2110C]

    _validate_ref_segments = root_validator(allow_reuse=True)(
        validate_duplicate_ref_codes
    )


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
    prv_segment: Optional[Loop2100BPrvSegment]

    _validate_ref_segments = root_validator(allow_reuse=True)(
        validate_duplicate_ref_codes
    )


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
