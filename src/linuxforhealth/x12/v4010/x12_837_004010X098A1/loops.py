"""
loops.py

Models the loops, or logical segment groupings, for the HealthCare Claims Professional 837 004010X098A1 transaction set.
The HealthCare Claims Professional set organizes loops into a hierarchical and nested model.

-- Header
    -- Loop 1000A (Submitter Name)
    -- Loop 1000B (Receiver Name)
    -- Loop 2000A (Billing / Pay to Provider)
        -- Loop 2010AA (Billing Provider Name)
        -- Loop 2010AB (Pay to Provider Name)
    -- Loop 2000B (Subscriber)
        -- Loop 2010BA (Subscriber Name)
        -- Loop 2010BB (Payer Name)
        -- Loop 2010BC (Reponsible Party Name)
        -- Loop 2000C (Patient)
            -- Loop 2010CA (Patient Name_
            -- Loop 2300 (Claim)
                -- Loop 2305 (Home Healthcare Plan Information)
                -- Loop 2310A (Referring Provider Name)
                -- Loop 2310B (Rendering Provider)
                -- Loop 2310C (Service Provider)
                -- Loop 2310D (Service Facility)
                -- Loop 2310E (Supervising Provider)
                -- Loop 2320 (Other Subscriber)
                -- Loop 2400 (Service Line)
                    -- Loop 2410 (Drug Identification)
                    -- Loop 2420a (Rendering Provider)
                    -- Loop 2420b (Purchased Service Provider)
                    -- Loop 2420c (Service Facility)
                    -- Loop 2420d (Supervising Provider)
                    -- Loop 2420e (Ordering Provider)
                    -- Loop 2420f (Referring Provider)
                    -- Loop 2420g (Other Payer)
                    -- Loop 2430 (Line Adjudication)
                    -- Loop 2440 (Form Identification)


-- Footer

The Header and Footer components are not "loops" per the specification, but are included to standardize and simplify
transactional modeling and processing.
"""
from decimal import Decimal

from linuxforhealth.x12.models import X12SegmentGroup
from .segments import (
    HeaderStSegment,
    HeaderBhtSegment,
    HeaderRefSegment,
    Loop1000ANm1Segment,
    Loop1000APerSegment,
    Loop1000BNm1Segment,
    Loop2000AHlSegment,
    Loop2000APrvSegment,
    Loop2010AaNm1Segment,
    Loop2010AaRefSegment,
    Loop2010AbNm1Segment,
    Loop2010AbRefSegment,
    Loop2000BHlSegment,
    Loop2000BSbrSegment,
    Loop2010BaNm1Segment,
    Loop2010BaRefSegment,
    Loop2010BbNm1Segment,
    Loop2010BbRefSegment,
    Loop2010BcNm1Segment,
    Loop2010BdNm1Segment,
    Loop2010BdRefSegment,
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
    Loop2305Cr7Segment,
    Loop2305HsdSegment,
    Loop2310ANm1Segment,
    Loop2310APrvSegment,
    Loop2310ARefSegment,
    Loop2310BNm1Segment,
    Loop2310BPrvSegment,
    Loop2310BRefSegment,
    Loop2310CNm1Segment,
    Loop2310CRefSegment,
    Loop2310DNm1Segment,
    Loop2310DRefSegment,
    Loop2310ENm1Segment,
    Loop2310ERefSegment,
    Loop2320SbrSegment,
    Loop2320AmtSegment,
    Loop2330aNm1Segment,
    Loop2330aRefSegment,
    Loop2330bNm1Segment,
    Loop2330BPerSegment,
    Loop2330BDtpSegment,
    Loop2300BRefSegment,
    Loop2330cNm1Segment,
    Loop2330cRefSegment,
    Loop2330dNm1Segment,
    Loop2330dRefSegment,
    Loop2330eNm1Segment,
    Loop2330eRefSegment,
    Loop2330fNm1Segment,
    Loop2330fRefSegment,
    Loop2330gNm1Segment,
    Loop2330gRefSegment,
    Loop2330HNm1Segment,
    Loop2330HRefSegment,
    Loop2400PwkSegment,
    Loop2400CrcSegment,
    Loop2400DtpSegment,
    Loop2400Cn1Segment,
    Loop2400RefSegment,
    Loop2400AmtSegment,
    Loop2400NteSegment,
    Loop2410RefSegment,
    Loop2420ANm1Segment,
    Loop2420APrvSegment,
    Loop2420ARefSegment,
    Loop2420BNm1Segment,
    Loop2420BRefSegment,
    Loop2420CNm1Segment,
    Loop2420CRefSegment,
    Loop2420DNm1Segment,
    Loop2420DRefSegment,
    Loop2420ENm1Segment,
    Loop2420ERefSegment,
    Loop2420EPerSegment,
    Loop2420FNm1Segment,
    Loop2420FPrvSegment,
    Loop2420FRefSegment,
    Loop2420GNm1Segment,
    Loop2420GRefSegment,
    Loop2430DtpSegment,
    Loop2010AaPerSegment,
)
from linuxforhealth.x12.v4010.segments import (
    SeSegment,
    CurSegment,
    N3Segment,
    N4Segment,
    PatSegment,
    DmgSegment,
    ClmSegment,
    K3Segment,
    Cr1Segment,
    Cr2Segment,
    HiSegment,
    CasSegment,
    OiSegment,
    MoaSegment,
    LxSegment,
    Sv1Segment,
    Sv5Segment,
    Cr3Segment,
    Cr5Segment,
    MeaSegment,
    Ps1Segment,
    HcpSegment,
    LinSegment,
    CtpSegment,
    SvdSegment,
    LqSegment,
    FrmSegment,
)
from typing import List, Optional, Dict
from pydantic import Field, root_validator
from linuxforhealth.x12.validators import (
    validate_duplicate_date_qualifiers,
    validate_duplicate_amt_codes,
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
    ref_segment: Optional[List[Loop2010AaRefSegment]] = Field(max_items=16)
    per_segment: Optional[List[Loop2010AaPerSegment]] = Field(max_items=2)


class Loop2010Ab(X12SegmentGroup):
    """
    Loop 2010AB - Pay to Provider Name
    """

    nm1_segment: Loop2010AbNm1Segment
    n3_segment: N3Segment
    n4_segment: N4Segment
    ref_segment: Optional[List[Loop2010AbRefSegment]] = Field(max_items=5)


class Loop2010Ba(X12SegmentGroup):
    """
    Loop 2010BA - Subscriber Name
    """

    nm1_segment: Loop2010BaNm1Segment
    n3_segment: Optional[N3Segment]
    n4_segment: Optional[N4Segment]
    dmg_segment: Optional[DmgSegment]
    ref_segment: Optional[List[Loop2010BaRefSegment]] = Field(max_items=5)


class Loop2010Bb(X12SegmentGroup):
    """
    Loop 2010Bb - Payer Name
    """

    nm1_segment: Loop2010BbNm1Segment
    n3_segment: Optional[N3Segment]
    n4_segment: Optional[N4Segment]
    ref_segment: Optional[List[Loop2010BbRefSegment]]


class Loop2010Bc(X12SegmentGroup):
    """
    Loop 2010Bc - Responsible Party Name
    """

    nm1_segment: Loop2010BcNm1Segment
    n3_segment: Optional[N3Segment]
    n4_segment: Optional[N4Segment]


class Loop2010Bd(X12SegmentGroup):
    """
    Credit/Debit Card Holder Name
    """

    nm1_segment: Loop2010BdNm1Segment
    ref_segment: Optional[List[Loop2010BdRefSegment]] = Field(max_items=2)


class Loop2305(X12SegmentGroup):
    """
    Home Health Care Plan Information
    """

    cr7_segment: Loop2305Cr7Segment
    hsd_segment: Optional[List[Loop2305HsdSegment]] = Field(max_items=3)


class Loop2330H(X12SegmentGroup):
    """
    Claim - Other Subscriber Other Payer Supervising Provider
    """

    nm1_segment: Loop2330HNm1Segment
    ref_segment: List[Loop2330HRefSegment] = Field(min_items=1, max_items=3)


class Loop2330G(X12SegmentGroup):
    """
    Claim - Other Subscriber Other Payer Billing Provider
    """

    nm1_segment: Loop2330gNm1Segment
    ref_segment: List[Loop2330gRefSegment] = Field(min_items=1, max_items=3)


class Loop2330F(X12SegmentGroup):
    """
    Claim - Other Subscriber Other Payer Purchased Service Provider
    """

    nm1_segment: Loop2330fNm1Segment
    ref_segment: List[Loop2330fRefSegment] = Field(min_items=1, max_items=3)


class Loop2330E(X12SegmentGroup):
    """
    Claim - Other Subscriber Other Payer Rendering Provider
    """

    nm1_segment: Loop2330eNm1Segment
    ref_segment: List[Loop2330eRefSegment] = Field(min_items=1, max_items=3)


class Loop2330D(X12SegmentGroup):
    """
    Claim - Other Subscriber Other Payer Referring Provider
    """

    nm1_segment: Loop2330dNm1Segment
    ref_segment: List[Loop2330dRefSegment] = Field(min_items=1, max_items=3)


class Loop2330C(X12SegmentGroup):
    """
    Claim - Other Subscriber Other Payer Patient Information
    """

    nm1_segment: Loop2330cNm1Segment
    ref_segment: List[Loop2330cRefSegment] = Field(min_items=1, max_items=3)


class Loop2330B(X12SegmentGroup):
    """
    Claim - Other Payer Name
    """

    nm1_segment: Loop2330bNm1Segment
    per_segment: Optional[List[Loop2330BPerSegment]] = Field(max_items=2)
    dtp_segment: Optional[Loop2330BDtpSegment]
    ref_segment: Optional[List[Loop2300BRefSegment]] = Field(max_items=6)


class Loop2330A(X12SegmentGroup):
    """
    Claim - Other Subscriber Name
    """

    nm1_segment: Loop2330aNm1Segment
    n3_segment: Optional[N3Segment]
    n4_segment: Optional[N4Segment]
    ref_segment: Optional[List[Loop2330aRefSegment]] = Field(max_items=3)


class Loop2320(X12SegmentGroup):
    """
    Claim Other subscriber information
    """

    sbr_segment: Loop2320SbrSegment
    cas_segment: Optional[List[CasSegment]] = Field(min_items=0, max_items=5)
    amt_segment: Optional[List[Loop2320AmtSegment]] = Field(min_items=0, max_items=8)
    oi_segment: Optional[OiSegment]
    moa_segment: Optional[MoaSegment]
    loop_2330a: Optional[Loop2330A]
    loop_2330b: Optional[Loop2330B]
    loop_2330c: Optional[List[Loop2330C]]
    loop_2330d: Optional[Loop2330D]
    loop_2330e: Optional[Loop2330E]
    loop_2330f: Optional[Loop2330F]
    loop_2330g: Optional[Loop2330G]
    loop_2330h: Optional[Loop2330H]

    _validate_amt_segments = root_validator(allow_reuse=True)(
        validate_duplicate_amt_codes
    )


class Loop2310E(X12SegmentGroup):
    """
    Supervising Provider Name
    """

    nm1_segment: Loop2310ENm1Segment
    ref_segment: Optional[List[Loop2310ERefSegment]] = Field(max_items=5)


class Loop2310D(X12SegmentGroup):
    """
    Service Facility Location
    """

    nm1_segment: Loop2310DNm1Segment
    n3_segment: N3Segment
    n4_segment: N4Segment
    ref_segment: Optional[List[Loop2310DRefSegment]]


class Loop2310C(X12SegmentGroup):
    """
    Purchased Service Provider Name
    """

    nm1_segment: Optional[Loop2310CNm1Segment]
    ref_segment: Optional[List[Loop2310CRefSegment]] = Field(max_items=3)


class Loop2310B(X12SegmentGroup):
    """
    Claim Rendering Provider
    """

    nm1_segment: Loop2310BNm1Segment
    prv_segment: Optional[Loop2310BPrvSegment]
    ref_segment: Optional[List[Loop2310BRefSegment]] = Field(max_items=4)


class Loop2310A(X12SegmentGroup):
    """
    Claim Referring Provider
    """

    nm1_segment: Loop2310ANm1Segment
    prv_segment: Loop2310APrvSegment
    ref_segment: Optional[List[Loop2310ARefSegment]] = Field(max_items=5)


class Loop2440(X12SegmentGroup):
    """
    Form Identification Code
    """

    lq_segment: LqSegment
    frm_segment: List[FrmSegment] = Field(min_items=1, max_items=99)


class Loop2430(X12SegmentGroup):
    """
    Claim Service Line - Adjudication Information
    """

    svd_segment: SvdSegment
    cas_segment: Optional[List[CasSegment]]
    dtp_segment: Loop2430DtpSegment


class Loop2420G(X12SegmentGroup):
    """
    Claim Service Line - Other Payer Prior Auth
    """

    nm1_segment: Loop2420GNm1Segment
    ref_segment: List[Loop2420GRefSegment] = Field(min_items=1, max_items=2)


class Loop2420F(X12SegmentGroup):
    """
    Claim Service Line - Referring Provider Name
    """

    nm1_segment: Loop2420FNm1Segment
    prv_segment: Optional[Loop2420FPrvSegment]
    ref_segment: Optional[List[Loop2420FRefSegment]] = Field(max_items=5)


class Loop2420E(X12SegmentGroup):
    """
    Claim Service Line - Ordering Provider Name
    """

    nm1_segment: Loop2420ENm1Segment
    n3_segment: Optional[N3Segment]
    n4_segment: Optional[N4Segment]
    ref_segment: Optional[List[Loop2420ERefSegment]] = Field(max_items=5)
    per_segment: Optional[Loop2420EPerSegment]


class Loop2420D(X12SegmentGroup):
    """
    Claim Service Line - Supervising Provider Name
    """

    nm1_segment: Loop2420DNm1Segment
    ref_segment: Optional[List[Loop2420DRefSegment]] = Field(max_items=5)


class Loop2420C(X12SegmentGroup):
    """
    Claim Service Line - Service Facility Location Name
    """

    nm1_segment: Loop2420CNm1Segment
    n3_segment: N3Segment
    n4_segment: N4Segment
    ref_segment: Optional[List[Loop2420CRefSegment]] = Field(max_items=5)


class Loop2420B(X12SegmentGroup):
    """
    Claim Service Line - Purchased Service Provider
    """

    nm1_segment: Loop2420BNm1Segment
    ref_segment: Optional[List[Loop2420BRefSegment]] = Field(max_items=5)


class Loop2420A(X12SegmentGroup):
    """
    Claim Service Line - Rendering Provider
    """

    nm1_segment: Loop2420ANm1Segment
    prv_segment: Optional[Loop2420APrvSegment]
    ref_segment: Optional[List[Loop2420ARefSegment]] = Field(max_items=5)


class Loop2410(X12SegmentGroup):
    """
    Claim Service Line - Drug Identification
    """

    lin_segment: LinSegment
    ctp_segment: CtpSegment
    ref_segment: Optional[Loop2410RefSegment]


class Loop2400(X12SegmentGroup):
    """
    Claim - Service Line
    """

    lx_segment: LxSegment
    sv1_segment: Sv1Segment
    sv5_segment: Optional[Sv5Segment]
    pwk_segment: Optional[List[Loop2400PwkSegment]] = Field(min_items=0, max_items=10)
    cr1_segment: Optional[Cr1Segment]
    cr2_segment: Optional[List[Cr2Segment]] = Field(max_items=5)
    cr3_segment: Optional[Cr3Segment]
    cr5_segment: Optional[Cr5Segment]
    crc_segment: Optional[List[Loop2400CrcSegment]] = Field(max_items=10)
    dtp_segment: List[Loop2400DtpSegment] = Field(min_items=1, max_items=20)
    mea_segment: Optional[List[MeaSegment]] = Field(max_items=20)
    cn1_segment: Optional[Loop2400Cn1Segment]
    ref_segment: Optional[List[Loop2400RefSegment]] = Field(max_items=15)
    amt_segment: Optional[List[Loop2400AmtSegment]] = Field(max_items=3)
    k3_segment: Optional[List[K3Segment]] = Field(max_items=10)
    nte_segment: Optional[Loop2400NteSegment]
    ps1_segment: Optional[Ps1Segment]
    hsd_segment: Optional[Loop2305HsdSegment]  # reusing segment
    hcp_segment: Optional[HcpSegment]
    loop_2410: Optional[Loop2410]
    loop_2420a: Optional[Loop2420A]
    loop_2420b: Optional[Loop2420B]
    loop_2420c: Optional[Loop2420C]
    loop_2420d: Optional[Loop2420D]
    loop_2420e: Optional[Loop2420E]
    loop_2420f: Optional[Loop2420F]
    loop_2420g: Optional[Loop2420G]
    loop_2430: Optional[List[Loop2430]]
    loop_2440: Optional[List[Loop2440]]

    _validate_dtp_qualifiers = root_validator(allow_reuse=True)(
        validate_duplicate_date_qualifiers
    )


class Loop2300(X12SegmentGroup):
    """
    Loop 2300 - Claims
    """

    clm_segment: ClmSegment
    dtp_segment: Optional[List[Loop2300DtpSegment]] = Field(min_items=0, max_items=17)
    pwk_segment: Optional[List[Loop2300PwkSegment]] = Field(min_items=0, max_items=10)
    cn1_segment: Optional[Loop2300Cn1Segment]
    amt_segment: Optional[List[Loop2300AmtSegment]] = Field(max_items=3)
    ref_segment: Optional[List[Loop2300RefSegment]] = Field(min_items=0, max_items=14)
    k3_segment: Optional[List[K3Segment]] = Field(min_items=0, max_items=10)
    nte_segment: Optional[Loop2300NteSegment]
    cr1_segment: Optional[Cr1Segment]
    cr2_segment: Optional[Cr2Segment]
    crc_segment: Optional[List[Loop2300CrcSegment]] = Field(min_items=0, max_items=8)
    hi_segment: Optional[List[HiSegment]] = Field(min_items=1, max_items=4)
    hcp_segment: Optional[HcpSegment]
    loop_2305: Optional[Loop2305]
    loop_2310a: Optional[Loop2310A]
    loop_2310b: Optional[Loop2310B]
    loop_2310c: Optional[Loop2310C]
    loop_2310d: Optional[Loop2310D]
    loop_2310e: Optional[Loop2310E]
    loop_2320: Optional[List[Loop2320]] = Field(min_items=0, max_items=10)
    loop_2400: List[Loop2400] = Field(min_items=1, max_items=50)

    _validate_dtp_qualifiers = root_validator(allow_reuse=True)(
        validate_duplicate_date_qualifiers
    )

    @root_validator
    def validate_claim_amounts(cls, values: Dict):
        """
        Validates that CLM02 == SUM(Loop2400.SV102)
        """
        claim_amount: Decimal = values.get("clm_segment").total_claim_charge_amount
        line_total: Decimal = Decimal("0.0")

        for line in values.get("loop_2400", []):
            line_total += line.sv1_segment.line_item_charge_amount

        if claim_amount != line_total:
            raise ValueError(
                f"Claim Amount {claim_amount} != Service Line Total {line_total}"
            )

        return values


class Loop2010Ca(X12SegmentGroup):
    """
    Loop 2010CA Patient Name
    """

    nm1_segment: Loop2010CaNm1Segment
    n3_segment: N3Segment
    n4_segment: N4Segment
    dmg_segment: DmgSegment
    ref_segment: Optional[List[Loop2010CaRefSegment]] = Field(max_items=6)


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
    loop_2010bc: Optional[Loop2010Bc]
    loop_2010bd: Optional[Loop2010Bd]
    loop_2300: Optional[List[Loop2300]] = Field(min_items=0, max_items=100)
    loop_2000c: Optional[List[Loop2000C]]


class Loop2000A(X12SegmentGroup):
    """
    Loop 2000A - Billing / Pay to Provider
    """

    hl_segment: Loop2000AHlSegment
    prv_segment: Optional[Loop2000APrvSegment]
    cur_segment: Optional[CurSegment]
    loop_2010aa: Loop2010Aa
    loop_2010ab: Optional[Loop2010Ab]
    loop_2000b: List[Loop2000B]


class Header(X12SegmentGroup):
    """
    Transaction Header Information
    """

    st_segment: HeaderStSegment
    bht_segment: HeaderBhtSegment
    ref_segment: HeaderRefSegment


class Footer(X12SegmentGroup):
    """
    Transaction Footer Information
    """

    se_segment: SeSegment
