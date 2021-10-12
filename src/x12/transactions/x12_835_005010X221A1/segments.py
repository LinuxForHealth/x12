"""
segments.py

Specialized segment models for the Health Care Claim Payment 835 005010X221A1 transaction set model.
"""
from x12.segments import (
    StSegment,
    TrnSegment,
    CurSegment,
    RefSegment,
    DtmSegment,
    PerSegment,
    N1Segment,
)
from typing import Literal, Optional
from enum import Enum


class HeaderStSegment(StSegment):
    transaction_set_identifier_code: Literal["835"]
    implementation_convention_reference: Optional[str]


class HeaderTrnSegment(TrnSegment):
    """
    Header Trace Segment
    """

    trace_type_code: Literal["1"]


class HeaderCurSegment(CurSegment):
    """
    Header Currency Segment
    """

    entity_identifier_code: Literal["PR"]


class HeaderRefSegment(RefSegment):
    """
    Header Ref Segments
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        RECEIVER_IDENTIFICATION_NUMBER = "EV"
        VERSION_CODE_LOCAL = "F2"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class HeaderDtmSegment(DtmSegment):
    """
    Header Dtm Segment
    """

    date_time_qualifier: Literal["405"]


class Loop1000AN1Segment(N1Segment):
    """
    Payer Identification
    """

    entity_identifier_code: Literal["PR"]
    identification_code_qualifier: Optional[Literal["XV"]]


class Loop1000ARefSegment(RefSegment):
    """
    Loop 1000A Ref Segment
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        PAYER_IDENTIFICATION_NUMBER = "2U"
        SUBMITTER_IDENTIFICATION_NUMBER = "EO"
        HEALTH_INDUSTRY_NUMBER = "HI"
        NAIC_CODE = "NF"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop1000APerSegment(PerSegment):
    """
    Loop 1000A Per Segment
    """

    class ContactFunctionCode(str, Enum):
        """
        Code values for PER01
        """

        PAYERS_CLAIM_OFFICE = "CX"
        TECHNICAL_DEPARTMENT = "BL"
        INFORMATION_CONTACT = "IC"

    contact_function_code: ContactFunctionCode


class Loop1000BN1Segment(N1Segment):
    """
    Payee Identification
    """

    class IdentificationCodeQualifier(str, Enum):
        """
        Code values for N1003
        """

        FEDERAL_TAXPAYER_IDENTIFICATION_NUMBER = "FI"
        CMS_PLAN_ID = "XV"
        CMS_NPI = "XX"

    entity_identifier_code: Literal["PE"]
    identification_code_qualifier: IdentificationCodeQualifier


class Loop1000BRefSegment(RefSegment):
    """
    Payee Reference Identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        STATE_LICENSE_NUMBER = "0B"
        NATIONAL_COUNCIL_PHARMACY_NUMBER = "D3"
        PAYEE_IDENTIFICATION = "PQ"
        FEDERAL_TAXPAYERS_IDENTIFICATION_NUMBER = "TJ"

    reference_identification_qualifier: ReferenceIdentificationQualifier
