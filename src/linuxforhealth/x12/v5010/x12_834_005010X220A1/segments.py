"""
segments.py

Specialized segment models for the Enrollment 834 005010X220A1 transaction.
"""
from typing import Literal
from enum import Enum

from linuxforhealth.x12.v5010.segments import (
    StSegment, RefSegment, DtpSegment, QtySegment
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
