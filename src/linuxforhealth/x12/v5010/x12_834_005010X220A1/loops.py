"""
loops.py

Models the loops, or logical segment groupings, for the Enrollment 834 005010X220A1 transaction set.

- Header
- Loop 1000A (Sponsor Name)
- Loop 1000B (Payer Name)
- Loop 1000C (TPA Broker Name)
    - Loop 1100C (TPA Broker Account Information)
- Loop 2000 (Member Level Detail)
    - Loop 2100A (Member Name)
    - Loop 2100B (Incorrect Member Name)
    - Loop 2100C (Member Mailing Address)
    - Loop 2100D (Member Employer)
    - Loop 2100E (Member School)
    - Loop 2100F (Custodial Parent)
    - Loop 2100G (Responsible Person)
    - Loop 2100H (Drop Off Location)
    - Loop 2200 (Disability Information)
    - Loop 2300 (Health Coverage)
        - Loop 2310 (Provider Information)
        - Loop 2320 (Coordination Of Benefits)
            - Loop 2330 (Coordination of Benefits Related Entity)
    - Loop 2700 (Member Reporting Categories)
        - Loop 2750 (Reporting Category)
- Footer

The Header and Footer components are not "loops" per the specification, but are included to standardize and simplify
transactional modeling and processing.
"""

from linuxforhealth.x12.models import X12SegmentGroup
from linuxforhealth.x12.v5010.segments import (
    SeSegment,
    ActSegment,
    N3Segment,
    N4Segment,
    EcSegment,
    IcmSegment,
    HlhSegment,
    LuiSegment,
)
from .segments import (
    HeaderStSegment,
    HeaderRefSegment,
    HeaderDtpSegment,
    HeaderQtySegment,
    Loop1000AN1Segment,
    Loop1000BN1Segment,
    Loop1000CN1Segment,
    Loop2000InsSegment,
    Loop2000RefSegment,
    Loop2000DtpSegment,
    Loop2100ANm1Segment,
    Loop2100APerSegment,
    Loop2100ADmgSegment,
    Loop2100AAmtSegment,
    Loop2100BNm1Segment,
    Loop2100BDmgSegment,
    Loop2100CNm1Segment,
    Loop2100DNm1Segment,
    Loop2100ENm1Segment,
    Loop2100FNm1Segment,
    Loop2100GNm1Segment,
    Loop2100HNm1Segment,
)
from typing import List, Optional
from pydantic import Field
from linuxforhealth.x12.v5010.segments import BgnSegment


class Header(X12SegmentGroup):
    """
    Transaction Header Information
    """

    st_segment: HeaderStSegment
    bgn_segment: BgnSegment
    ref_segment: Optional[HeaderRefSegment]
    dtp_segment: Optional[List[HeaderDtpSegment]] = Field(max_items=6)
    qty_segment: Optional[List[HeaderQtySegment]] = Field(max_items=3)


class Loop1000A(X12SegmentGroup):
    """
    Sponsor Name
    """

    n1_segment: Loop1000AN1Segment


class Loop1000B(X12SegmentGroup):
    """
    Payer
    """

    n1_segment: Loop1000BN1Segment


class Loop1100C(X12SegmentGroup):
    """
    TPA/Broker Account Information
    """

    act_segment: ActSegment


class Loop1000C(X12SegmentGroup):
    """
    TPA/Broker Name
    """

    n1_segment: Loop1000CN1Segment
    loop_1100c: Optional[Loop1100C]


class Loop2100A(X12SegmentGroup):
    """
    Member Name
    """

    nm1_segment: Loop2100ANm1Segment
    per_segment: Optional[Loop2100APerSegment]
    n3_segment: Optional[N3Segment]
    n4_segment: Optional[N4Segment]
    dmg_segment: Optional[Loop2100ADmgSegment]
    ec_segment: Optional[List[EcSegment]]
    icm_segment: Optional[IcmSegment]
    amt_segment: Optional[List[Loop2100AAmtSegment]]
    hlh_segment: Optional[HlhSegment]
    lui_segment: Optional[List[LuiSegment]]


class Loop2100B(X12SegmentGroup):
    """
    Incorrect Member Name
    """

    nm1_segment: Loop2100BNm1Segment
    dmg_segment: Loop2100BDmgSegment


class Loop2100C(X12SegmentGroup):
    """
    Member Mailing Address
    """

    nm1_segment: Loop2100CNm1Segment
    n3_segment: N3Segment
    n4_segment: N4Segment


class Loop2100D(X12SegmentGroup):
    """
    Member Employer
    """

    nm1_segment: Loop2100DNm1Segment
    # reusing PER segment as communication qualifiers are the same
    per_segment: Loop2100APerSegment
    n3_segment: N3Segment
    n4_segment: N4Segment


class Loop2100E(X12SegmentGroup):
    """
    Member School
    """

    nm1_segment: Loop2100ENm1Segment
    # reusing PER segment as communication qualifiers are the same
    per_segment: Loop2100APerSegment
    n3_segment: N3Segment
    n4_segment: N4Segment


class Loop2100F(X12SegmentGroup):
    """
    Member Custodial Parent
    """

    nm1_segment: Loop2100FNm1Segment
    # reusing PER segment as communication qualifiers are the same
    per_segment: Loop2100APerSegment
    n3_segment: N3Segment
    n4_segment: N4Segment


class Loop2100G(X12SegmentGroup):
    """
    Member Responsible Parent
    """

    nm1_segment: Loop2100GNm1Segment
    # reusing PER segment as communication qualifiers are the same
    per_segment: Loop2100APerSegment
    n3_segment: N3Segment
    n4_segment: N4Segment


class Loop2100H(X12SegmentGroup):
    """
    Member drop off location
    """

    nm1_segment: Loop2100HNm1Segment
    n3_segment: N3Segment
    n4_segment: N4Segment


class Loop2000(X12SegmentGroup):
    """
    Member Level Detail
    """

    ins_segment: Loop2000InsSegment
    ref_segment: List[Loop2000RefSegment]
    dtp_segment: Optional[List[Loop2000DtpSegment]]
    loop_2100a: Loop2100A
    loop_2100b: Optional[Loop2100B]
    loop_2100c: Optional[Loop2100C]
    loop_2100d: Optional[List[Loop2100D]] = Field(max_items=3)
    loop_2100e: Optional[Loop2100E]
    loop_2100f: Optional[Loop2100F]
    loop_2100g: Optional[Loop2100G]
    loop_2100h: Optional[Loop2100H]


class Footer(X12SegmentGroup):
    """
    Transaction Footer Information
    """

    se_segment: SeSegment
