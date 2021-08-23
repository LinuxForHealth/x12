"""
loops.py

Models the loops, or logical segment groupings, for the Eligibility 271 005010X279A1 transaction set.
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
    MpiSegment,
    EbSegment,
    HsdSegment,
    MsgSegment,
    IiiSegment,
    LsSegment,
    LeSegment,
    PerSegment,
    PrvSegment,
)
from .segments import (
    HeaderStSegment,
    HeaderBhtSegment,
    Loop2000CHlSegment,
    Loop2100BNm1Segment,
    Loop2000BHlSegment,
    Loop2100BRefSegment,
    Loop2100BPrvSegment,
    Loop2100ANm1Segment,
    Loop2000AHlSegment,
    Loop2000AAaaSegment,
    Loop2100CNm1Segment,
    Loop2100RefSegment,
    Loop2100CInsSegment,
    Loop2100DtpSegment,
    Loop2110RefSegment,
    Loop2110DtpSegment,
    Loop2100AAaaSegment,
    Loop2100BAaaSegment,
    Loop2110CAaaSegment,
    Loop2120Nm1Segment,
    Loop2000DHlSegment,
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


class Loop2120D(X12SegmentGroup):
    """
    Loop 2120D
    """

    nm1_segment: Loop2120Nm1Segment
    n3_segment: Optional[N3Segment]
    n4_segment: Optional[N4Segment]
    per_segment: Optional[List[PerSegment]] = Field(min_items=0, max_items=3)
    prv_segment: Optional[PrvSegment]


class Loop2115D(X12SegmentGroup):
    """
    Loop 2115D - Dependent Eligibility or Benefit Additional Information
    """

    iii_segment: IiiSegment
    ls_segment: LsSegment
    loop_2120c: Optional[List[Loop2120D]] = Field(min_items=0, max_items=23)
    le_segment: LeSegment


class Loop2110D(X12SegmentGroup):
    """
    Loop 2110D Dependent Eligibility or Benefit Information
    """

    eb_segment: EbSegment
    hsd_segment: Optional[List[HsdSegment]] = Field(min_items=0, max_items=9)
    ref_segment: Optional[List[Loop2110RefSegment]] = Field(min_items=0, max_items=9)
    dtp_segment: Optional[List[Loop2110DtpSegment]] = Field(min_items=0, max_items=20)
    aaa_segment: Optional[List[Loop2110CAaaSegment]] = Field(min_items=0, max_items=9)
    msg_segment: Optional[List[MsgSegment]] = Field(min_items=0, max_items=10)
    loop_2115d: Optional[List[Loop2115D]] = Field(min_items=0, max_items=10)
    ls_segment: Optional[LsSegment]
    loop_2120d: Optional[List[Loop2120D]] = Field(min_items=0, max_items=23)
    le_segment: Optional[LeSegment]

    _validate_ref_segments = root_validator(allow_reuse=True)(
        validate_duplicate_ref_codes
    )


class Loop2100D(X12SegmentGroup):
    """
    Loop 2100D - Dependent Name
    """

    nm1_segment: Loop2100CNm1Segment
    ref_segment: Optional[List[Loop2100RefSegment]] = Field(min_items=0, max_items=9)
    n3_segment: Optional[N3Segment]
    n4_segment: Optional[N4Segment]
    # Loop2100D AAA is identical to Loop2100B AAA
    aaa_segment: Optional[List[Loop2100BAaaSegment]] = Field(min_items=0, max_items=9)
    prv_segment: Optional[PrvSegment]
    dmg_segment: Optional[DmgSegment]
    ins_segment: Optional[Loop2100CInsSegment]
    hi_segment: Optional[HiSegment]
    dtp_segment: Optional[List[Loop2100DtpSegment]] = Field(min_items=0, max_items=9)
    mpi_segment: Optional[MpiSegment]
    loop_2110d: Optional[List[Loop2110D]] = Field(min_items=0)

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


class Loop2120C(X12SegmentGroup):
    """
    Loop 2120C Subscriber Benefit Related Entity Name
    """

    nm1_segment: Loop2120Nm1Segment
    n3_segment: Optional[N3Segment]
    n4_segment: Optional[N4Segment]
    per_segment: Optional[List[PerSegment]] = Field(min_items=0, max_items=3)
    prv_segment: Optional[PrvSegment]


class Loop2115C(X12SegmentGroup):
    """
    Loop 2115C - Subscriber Eligibility or Benefit Information Additional Information
    """

    iii_segment: IiiSegment
    ls_segment: LsSegment
    loop_2120c: Optional[List[Loop2120C]] = Field(min_items=0, max_items=23)
    le_segment: LeSegment


class Loop2110C(X12SegmentGroup):
    """
    Loop2110C - Subscriber Eligibility or Benefit Information
    """

    eb_segment: EbSegment
    hsd_segment: Optional[List[HsdSegment]] = Field(min_items=0, max_items=9)
    ref_segment: Optional[List[Loop2110RefSegment]] = Field(min_items=0, max_items=9)
    dtp_segment: Optional[List[Loop2110DtpSegment]] = Field(min_items=0, max_items=20)
    aaa_segment: Optional[List[Loop2110CAaaSegment]] = Field(min_items=0, max_items=9)
    msg_segment: Optional[List[MsgSegment]] = Field(min_items=0, max_items=10)
    loop_2115c: Optional[List[Loop2115C]] = Field(min_items=0, max_items=10)
    ls_segment: Optional[LsSegment]
    loop_2120c: Optional[List[Loop2120C]] = Field(min_items=0, max_items=23)
    le_segment: Optional[LeSegment]

    _validate_ref_segments = root_validator(allow_reuse=True)(
        validate_duplicate_ref_codes
    )

    @root_validator
    def validate_red_cross_eb_ref_codes(cls, values):
        """
        Validates that reference identification codes are limited when American Red Cross is the eligibility benefit.

        :@param values: The validated model values
        """
        benefit_code = values["eb_segment"].eligibility_benefit_information
        arc_ref_types = {"1W", "49", "F6", "NQ"}
        ref_types = {
            r.reference_identification_qualifier for r in values.get("ref_segments", [])
        }

        if ref_types and benefit_code == "R" and (ref_types - arc_ref_types):
            raise ValueError(f"{ref_types} are not valid for American Red Cross")

        return values


class Loop2100C(X12SegmentGroup):
    """
    Loop 2100C - Subscriber Name
    """

    nm1_segment: Loop2100CNm1Segment
    ref_segment: Optional[List[Loop2100RefSegment]] = Field(min_items=0, max_items=9)
    n3_segment: Optional[N3Segment]
    n4_segment: Optional[N4Segment]
    # Loop2100C AAA is identical to Loop2100B AAA
    aaa_segment: Optional[List[Loop2100BAaaSegment]] = Field(min_items=0, max_items=9)
    prv_segment: Optional[PrvSegment]
    dmg_segment: Optional[DmgSegment]
    ins_segment: Optional[Loop2100CInsSegment]
    hi_segment: Optional[HiSegment]
    dtp_segment: Optional[List[Loop2100DtpSegment]] = Field(min_items=0, max_items=9)
    mpi_segment: Optional[MpiSegment]
    loop_2110c: Optional[List[Loop2110C]] = Field(min_items=0)

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
    aaa_segment: Optional[Loop2100BAaaSegment]
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
    prv_segment: Optional[List[PrvSegment]] = Field(min_items=0, max_items=3)
    aaa_segment: Optional[List[Loop2100AAaaSegment]] = Field(min_items=0, max_items=9)


class Loop2000A(X12SegmentGroup):
    """
    Loop 2000A - Information Source
    The root node/loop for the 271 transaction

    """

    hl_segment: Loop2000AHlSegment
    aaa_segment: Optional[List[Loop2000AAaaSegment]] = Field(min_items=0, max_items=9)
    loop_2100a: Loop2100A
    loop_2000b: List[Loop2000B] = Field(min_items=0)


class Footer(X12SegmentGroup):
    """
    Transaction Footer Information
    """

    se_segment: SeSegment
