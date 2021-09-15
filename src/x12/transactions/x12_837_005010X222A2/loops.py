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
            -- Loop 2000C (Patient Loop)
                -- Loop 2010CA (Patient Name)
                -- Loop 2300 (Claim Information)
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
)
from x12.segments import SeSegment, CurSegment
from typing import List, Optional
from pydantic import Field


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


class Loop2000A(X12SegmentGroup):
    """
    Loop 2000A - Billing Provider
    """

    hl_segment: Loop2000AHlSegment
    prv_segment: Loop2000APrvSegment
    cur_segment: Optional[CurSegment]


class Header(X12SegmentGroup):
    """
    Transaction Header Information
    """

    st_segment: HeaderStSegment
    bht_segment: HeaderBhtSegment
    loop_1000a: Loop1000A
    loop_1000b: Loop1000B
    loop_2000a: List[Loop2000A] = Field(min_items=1)


class Footer(X12SegmentGroup):
    """
    Transaction Footer Information
    """

    se_segment: SeSegment
