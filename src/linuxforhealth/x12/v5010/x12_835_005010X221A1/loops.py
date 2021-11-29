"""
loops.py

Models the loops, or logical segment groupings, for the Health Care Claim Payment 835 005010X221A1 transaction set model.
The Health Care Claim Payment transaction set organizes loops into a hierarchical and nested model.
"""
from linuxforhealth.x12.models import X12SegmentGroup
from linuxforhealth.x12.v5010.segments import (
    SeSegment,
    BprSegment,
    DtmSegment,
    N3Segment,
    N4Segment,
    RdmSegment,
    LxSegment,
    Ts3Segment,
    Ts2Segment,
    ClpSegment,
    Nm1Segment,
    MiaSegment,
    MoaSegment,
    SvcSegment,
    PlbSegment,
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
    Loop2100CasSegment,
    Loop2100RefSegment,
    Loop2100DtmSegment,
    Loop2100PerSegment,
    Loop2100AmtSegment,
    Loop2100QtySegment,
    Loop2110DtmSegment,
    Loop2110CasSegment,
    Loop2110RefSegment,
    Loop2110AmtSegment,
    Loop2110QtySegment,
    Loop2110LqSegment,
)
from typing import Optional, List
from pydantic import Field, root_validator
from decimal import Decimal


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


class Loop2110(X12SegmentGroup):
    """
    Loop 2110 - Service Line Payment Information
    """

    svc_segment: SvcSegment
    dtm_segment: Optional[List[Loop2110DtmSegment]] = Field(min_items=0, max_items=2)
    cas_segment: Optional[List[Loop2110CasSegment]] = Field(min_items=0, max_items=99)
    ref_segment: Optional[List[Loop2110RefSegment]] = Field(min_items=0, max_items=24)
    amt_segment: Optional[List[Loop2110AmtSegment]] = Field(min_items=0, max_items=9)
    qty_segment: Optional[List[Loop2110QtySegment]] = Field(min_items=0, max_items=6)
    lq_segment: Optional[List[Loop2110LqSegment]] = Field(min_items=0, max_items=99)


class Loop2100(X12SegmentGroup):
    """
    Loop 2100 - Claim Payment Information
    """

    clp_segment: ClpSegment
    cas_segment: Optional[List[Loop2100CasSegment]] = Field(min_items=0, max_items=99)
    nm1_segment: List[Nm1Segment] = Field(min_items=1, max_items=7)
    mia_segment: Optional[MiaSegment]
    moa_segment: Optional[MoaSegment]
    ref_segment: Optional[List[Loop2100RefSegment]] = Field(min_items=0, max_items=15)
    dtm_segment: Optional[List[Loop2100DtmSegment]] = Field(min_items=0, max_items=5)
    per_segment: Optional[List[Loop2100PerSegment]] = Field(min_items=0, max_items=2)
    amt_segment: Optional[List[Loop2100AmtSegment]] = Field(min_items=0, max_items=13)
    qty_segment: Optional[List[Loop2100QtySegment]] = Field(min_items=0, max_items=14)
    loop_2110: Optional[List[Loop2110]] = Field(min_items=0, max_items=99)

    @root_validator
    def validate_balance(cls, values):
        """
        Validates the claim totals reported in the CLP segment against the adjustments made in CAS segments.
        The balance is calculated as:
            clp.charge amount - cas.adjustments = clp.payment_amount

        CAS segments exist within loops 2100 and 2110
        """
        clp_segment = values.get("clp_segment")
        if not clp_segment:
            return values
        charge_amount = clp_segment.total_claim_charge_amount
        payment_amount = clp_segment.claim_payment_amount
        adjustment_amount = Decimal("0.0")

        cas_segments = values.get("cas_segment", [])
        for adjustment in cas_segments:
            adjustment_data = adjustment.dict()
            for i in range(1, 7, 1):
                amount = adjustment_data.get(f"monetary_amount_{i}")
                adjustment_amount += amount if amount else Decimal("0.0")

        loop_2110 = values.get("loop_2110") or []
        for service_payment in loop_2110:
            adjustments = service_payment.cas_segment or []
            for adjustment in adjustments:
                adjustment_data = adjustment.dict()
                for i in range(1, 7, 1):
                    amount = adjustment_data.get(f"monetary_amount_{i}")
                    adjustment_amount += amount if amount else Decimal("0.0")

        if charge_amount - payment_amount != adjustment_amount:
            raise ValueError(
                f"Unable to balance charge amount {charge_amount} paid amount {payment_amount} against adjustments {adjustment_amount}"
            )

        return values


class Loop2000(X12SegmentGroup):
    """
    Loop 2000 - Claim Payment Header Number
    """

    lx_segment: LxSegment
    ts3_segment: Optional[Ts3Segment]
    ts2_segment: Optional[Ts2Segment]
    loop_2100: List[Loop2100]


class Footer(X12SegmentGroup):
    """
    Transaction Footer Information
    """

    plb_segment: Optional[PlbSegment]
    se_segment: SeSegment
