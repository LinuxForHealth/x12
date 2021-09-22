"""
loops.py

Models the loops, or logical segment groupings, for the HealthCare Claims Professional 837 005010X222A2 transaction set.
The HealthCare Claims Professional set organizes loops into a hierarchical and nested model.

-- Header
    -- Loop 1000A (Submitter Name)
        -- Loop 1000B (Receiver Name)
    -- Loop 2000A (Billing Provider)
        -- Loop 2010AA (Billing Provider Name)
        -- Loop 2010AB (Pay to Address)
        -- Loop 2010AC (Pay to Plan Name)
        -- Loop 2000B (Subscriber)
            -- Loop 2010BA (Subscriber Name)
            -- Loop 2010BB (Payer Name)
        -- Loop 2000C (Patient Loop)
            -- Loop 2010CA (Patient Name)
            -- Loop 2300 (Claim Information)
                -- Loop 2310A (Referring Provider Name)
                -- Loop 2310B (Rendering Provider Name)
                -- Loop 2310C (Service Facility Location Name)
                -- Loop 2310D (Supervising Provider Name)
                -- Loop 2310E (Ambulance Pickup Location)
                -- Loop 2310F (Ambulance Dropoff Location)
                -- Loop 2320 (Other Subscriber Information)
                    -- Loop 2330A (Other Subscriber Name)
                    -- Loop 2330B (Other Payer Name)
                    -- Loop 2330C (Other Payer Referring Provider Name)
                    -- Loop 2330D (Other Payer Rendering Provider Name)
                    -- Loop 2330E (Other Payer Service Facility Location)
                    -- Loop 2330F (Other Payer Supervising Provider Name)
                    -- Loop 2330G (Other Payer Billing Provider Name)
                -- Loop 2400 (Service Line)
                    -- Loop 2410 (Drug Identification Name)
                    -- Loop 2420A (Rendering Provider Name)
                    -- Loop 2420B (Purchased Service Provider Name)
                    -- Loop 2420C (Service Facility Location Name)
                    -- Loop 2420D (Supervising Provider Name)
                    -- Loop 2420E (Ordering Provider Name)
                    -- Loop 2420F (Referring Provider Name)
                    -- Loop 2420G (Ambulance Pickup Location)
                    -- Loop 2420H (Ambulance Dropoff Location)
                    -- Loop 2430 (Line Adjudication Information)
                    -- Loop 2440 (Form Identification)
-- Footer

The Header and Footer components are not "loops" per the specification, but are included to standardize and simplify
transactional modeling and processing.
"""
from x12.models import X12SegmentGroup
from .segments import (
    HeaderStSegment,
    HeaderBhtSegment,
    Loop1000ANm1Segment,
    Loop1000APerSegment,
    Loop1000BNm1Segment,
    Loop2000AHlSegment,
    Loop2000APrvSegment,
    Loop2010AaNm1Segment,
    Loop2010AaRefSegment,
    Loop2010AbNm1Segment,
    Loop2010AcNm1Segment,
    Loop2000BHlSegment,
    Loop2000BSbrSegment,
    Loop2010BaNm1Segment,
    Loop2010BaPerSegment,
    Loop2010BbNm1Segment,
    Loop2010BbRefSegment,
    Loop2300DtpSegment,
    Loop2300PwkSegment,
    Loop2300Cn1Segment,
    Loop2300AmtSegment,
    Loop2300RefSegment,
    Loop2300NteSegment,
    Loop2300CrcSegment,
    Loop2000CHlSegment,
    Loop2000CPatSegment,
    Loop2010CaNm1Segment,
    Loop2010CaRefSegment,
    Loop2010CaPerSegment,
    Loop2300HcpSegment,
    Loop2310ANm1Segment,
    Loop2310ARefSegment,
    Loop2310BNm1Segment,
    Loop2310BPrvSegment,
    Loop2310BRefSegment,
)
from x12.segments import (
    SeSegment,
    CurSegment,
    N3Segment,
    N4Segment,
    PatSegment,
    DmgSegment,
    RefSegment,
    ClmSegment,
    K3Segment,
    Cr1Segment,
    Cr2Segment,
    HiSegment,
)
from typing import List, Optional
from pydantic import Field, root_validator
from x12.validators import (
    validate_duplicate_ref_codes,
    validate_duplicate_date_qualifiers,
)


class Loop1000A(X12SegmentGroup):
    """
    Loop 1000A - Submitter Name
    """

    nm1_segment: Loop1000ANm1Segment
    per_segment: List[Loop1000APerSegment] = Field(min_items=1, max_items=2)


class Loop1000B(X12SegmentGroup):
    """
    Loop 1000B - Receiver Name
    """

    nm1_segment: Loop1000BNm1Segment


class Loop2010Aa(X12SegmentGroup):
    """
    Loop 2010AA - Billing Provider Name
    """

    nm1_segment: Loop2010AaNm1Segment
    n3_segment: N3Segment
    n4_segment: N4Segment
    ref_segment: List[Loop2010AaRefSegment] = Field(min_items=1, max_items=3)

    _validate_ref_segments = root_validator(allow_reuse=True)(
        validate_duplicate_ref_codes
    )


class Loop2010Ab(X12SegmentGroup):
    """
    Loop 2010AB - Pay to Address
    """

    nm1_segment: Loop2010AbNm1Segment
    n3_segment: N3Segment
    n4_segment: N4Segment


class Loop2010Ac(X12SegmentGroup):
    """
    Loop 2010AC - Pay to Plan
    """

    nm1_segment: Loop2010AcNm1Segment
    n3_segment: N3Segment
    n4_segment: N4Segment
    ref_segment: List[Loop2010AaRefSegment] = Field(min_items=1, max_items=2)

    _validate_ref_segments = root_validator(allow_reuse=True)(
        validate_duplicate_ref_codes
    )


class Loop2010Ba(X12SegmentGroup):
    """
    Loop 2010BA - Subscriber Name
    """

    nm1_segment: Loop2010BaNm1Segment
    n3_segment: Optional[N3Segment]
    n4_segment: Optional[N4Segment]
    dmg_segment: Optional[DmgSegment]
    ref_segment: List[Optional[RefSegment]] = Field(min_items=0, max_items=2)
    per_segment: Optional[Loop2010BaPerSegment]

    _validate_ref_segments = root_validator(allow_reuse=True)(
        validate_duplicate_ref_codes
    )


class Loop2010Bb(X12SegmentGroup):
    """
    Loop 2010Bb - Payer Name
    """

    nm1_segment: Loop2010BbNm1Segment
    n3_segment: Optional[N3Segment]
    n4_segment: Optional[N4Segment]
    ref_segment: Optional[List[Loop2010BbRefSegment]]

    _validate_ref_segments = root_validator(allow_reuse=True)(
        validate_duplicate_ref_codes
    )


class Loop2310B(X12SegmentGroup):
    """
    Claim Rendering Provider
    """

    nm1_segment: Loop2310BNm1Segment
    prv_segment: Optional[Loop2310BPrvSegment]
    ref_segment: Optional[List[Loop2310BRefSegment]] = Field(min_items=0, max_items=4)

    _validate_duplicate_ref_codes = root_validator(allow_reuse=True)(
        validate_duplicate_ref_codes
    )


class Loop2310A(X12SegmentGroup):
    """
    Claim Referring Provider
    """

    nm1_segment: Loop2310ANm1Segment
    ref_segment: Optional[List[Loop2310ARefSegment]] = Field(min_items=0, max_items=3)

    _validate_duplicate_ref_codes = root_validator(allow_reuse=True)(
        validate_duplicate_ref_codes
    )


class Loop2300(X12SegmentGroup):
    """
    Loop 2300 - Claims
    """

    clm_segment: ClmSegment
    dtp_segment: Optional[List[Loop2300DtpSegment]] = Field(min_items=0, max_items=17)
    pwk_segment: Optional[List[Loop2300PwkSegment]] = Field(min_items=0, max_items=10)
    cn1_segment: Optional[Loop2300Cn1Segment]
    amt_segment: Optional[Loop2300AmtSegment]
    ref_segment: Optional[List[Loop2300RefSegment]] = Field(min_items=0, max_items=14)
    k3_segment: Optional[List[K3Segment]] = Field(min_items=0, max_items=10)
    nte_segment: Optional[Loop2300NteSegment]
    cr1_segment: Optional[Cr1Segment]
    cr2_segment: Optional[Cr2Segment]
    crc_segment: Optional[List[Loop2300CrcSegment]] = Field(min_items=0, max_items=8)
    hi_segment: Optional[List[HiSegment]] = Field(min_items=1, max_items=4)
    hcp_segment: Optional[Loop2300HcpSegment]
    loop_2310a: Optional[Loop2310A]
    loop_2310b: Optional[Loop2310B]

    _validate_dtp_qualifiers = root_validator(allow_reuse=True)(
        validate_duplicate_date_qualifiers
    )

    _validate_duplicate_ref_codes = root_validator(allow_reuse=True)(
        validate_duplicate_ref_codes
    )


class Loop2010Ca(X12SegmentGroup):
    """
    Loop 2010CA Patient Name
    """

    nm1_segment: Loop2010CaNm1Segment
    n3_segment: N3Segment
    n4_segment: N4Segment
    dmg_segment: DmgSegment
    ref_segment: Optional[List[Loop2010CaRefSegment]] = Field(min_items=0, max_items=2)
    per_segment: Optional[Loop2010CaPerSegment]


class Loop2000C(X12SegmentGroup):
    """
    Loop 2000C - Patient
    """

    hl_segment: Loop2000CHlSegment
    pat_segment: Loop2000CPatSegment
    loop_2010ca: Loop2010Ca
    loop_2300: Optional[List[Loop2300]] = Field(min_items=0, max_items=100)


class Loop2000B(X12SegmentGroup):
    """
    Loop 2000B - Subscriber
    """

    hl_segment: Loop2000BHlSegment
    sbr_segment: Loop2000BSbrSegment
    pat_segment: Optional[PatSegment]
    loop_2010ba: Loop2010Ba
    loop_2010bb: Loop2010Bb
    # todo: validate 2300 based on 2010ba nm1 member id and patient loop
    loop_2300: Optional[List[Loop2300]] = Field(min_items=0, max_items=100)
    loop_2000c: Optional[List[Loop2000C]]


class Loop2000A(X12SegmentGroup):
    """
    Loop 2000A - Billing Provider
    """

    hl_segment: Loop2000AHlSegment
    prv_segment: Loop2000APrvSegment
    cur_segment: Optional[CurSegment]
    loop_2010aa: Loop2010Aa
    loop_2010ab: Loop2010Ab
    loop_2010ac: Optional[Loop2010Ac]
    loop_2000b: List[Loop2000B]


class Header(X12SegmentGroup):
    """
    Transaction Header Information
    """

    st_segment: HeaderStSegment
    bht_segment: HeaderBhtSegment


class Footer(X12SegmentGroup):
    """
    Transaction Footer Information
    """

    se_segment: SeSegment
