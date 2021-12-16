"""
segments.py

Specialized segment models for the Enrollment 834 005010X220A1 transaction.
"""
from typing import Literal, Optional
from enum import Enum
from pydantic import Field

from linuxforhealth.x12.v5010.segments import (
    StSegment,
    RefSegment,
    DtpSegment,
    QtySegment,
    N1Segment
)


class HeaderStSegment(StSegment):
    """
    Customized ST segment for 834 transaction header
    """

    transaction_set_identifier_code: Literal["834"]
    implementation_convention_reference: Literal["005010X220A1"]


class HeaderRefSegment(RefSegment):
    """
    Transaction Set Policy Number
    """

    reference_identification_qualifier: Literal["38"]


class HeaderDtpSegment(DtpSegment):
    """
    File Effective Date
    """

    class DateTimeQualifier(str, Enum):
        """
        DTP01 code values
        """

        EFFECTIVE = "007"
        REPORT_START = "090"
        REPORT_END = "091"
        MAINTENANCE_EFFECTIVE = "303"
        ENROLLMENT = "382"
        PAYMENT_COMMENCEMENT = "388"

    date_time_qualifier: DateTimeQualifier
    date_time_period_format_qualifier: Literal["D8"]


class HeaderQtySegment(QtySegment):
    """
    Transaction Set Control Totals
    """

    class QuantityQualifier(str, Enum):
        """
        Code values for QTY01
        """

        DEPENDENT_TOTAL = "DT"
        EMPLOYEE_TOTAL = "ET"
        TOTAL = "TO"

    quantity_qualifier: QuantityQualifier


class Loop1000AN1Segment(N1Segment):
    """
    Loop 1000A Sponsor Name
    """
    class IdentificationCodeQualifier(str, Enum):
        """
        Code values for N103
        """
        EMPLOYER_IDENTIFICATION_NUMBER = "24"
        ORGANIZATION_ASSIGNED_CODE = "94"
        FEDERAL_TAXPAYER_IDENTIFICATION_NUMBER = "FI"

    entity_identifier_code: Literal["P5"]
    name: Optional[str] = Field(min_length=1, max_length=60)
    identification_code_qualifier: IdentificationCodeQualifier


class Loop1000BN1Segment(N1Segment):
    """
    Loop 1000B Payer Name
    """
    class IdentificationCodeQualifier(str, Enum):
        """
        Code values for N103
        """
        ORGANIZATION_ASSIGNED_CODE = "94"
        FEDERAL_TAXPAYER_IDENTIFICATION_NUMBER = "FI"
        CMS_PLAN_ID = "XV"

    entity_identifier_code: Literal["IN"]
    name: Optional[str] = Field(min_length=1, max_length=60)
    identification_code_qualifier: IdentificationCodeQualifier


class Loop1000CN1Segment(N1Segment):
    """
    Loop 1000C TPA/Broker Name
    """
    class EntityIdentifierCode(str, Enum):
        """
        Code values for N101
        """
        BROKER_SALES_OFFICE = "BO"
        THIRD_PARTY_ADMINISTRATOR = "TV"

    class IdentificationCodeQualifier(str, Enum):
        """
        Code values for N103
        """
        ORGANIZATION_ASSIGNED_CODE = "94"
        FEDERAL_TAXPAYER_IDENTIFICATION_NUMBER = "FI"
        CMS_PLAN_ID = "XV"

    entity_identifier_code: EntityIdentifierCode
    identification_code_qualifier: IdentificationCodeQualifier


