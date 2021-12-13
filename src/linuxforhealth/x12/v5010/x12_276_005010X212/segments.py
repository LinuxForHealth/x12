"""
segments.py

Specialized segment models for the Health Care Claim Status Request 276 005010X212 transaction.
"""
from linuxforhealth.x12.v5010.segments import (
    StSegment,
    BhtSegment,
    HlSegment,
    Nm1Segment,
    DmgSegment,
    TrnSegment,
    RefSegment,
    AmtSegment,
    DtpSegment,
    SvcSegment,
)
from typing import Literal, Optional, Union
from enum import Enum
import datetime
from decimal import Decimal


class HeaderStSegment(StSegment):
    """
    Customized ST segment for 837 transaction header
    """

    transaction_set_identifier_code: Literal["276"]
    implementation_convention_reference: Literal["005010X212"]


class HeaderBhtSegment(BhtSegment):
    """
    Header BHT Segment
    """

    hierarchical_structure_code: Literal["0010"]
    transaction_set_purpose_code: Literal["13"]
    transaction_type_code: Optional[str]


class Loop2000AHlSegment(HlSegment):
    """
    Information Source HL Segment
    """

    hierarchical_level_code: Literal["20"]
    hierarchical_parent_id_number: Optional[str]
    hierarchical_child_code: Literal["1"]


class Loop2100ANm1Segment(Nm1Segment):
    """
    Payer Name
    """

    class IdentificationCodeQualifier(str, Enum):
        """
        Code values for NM108
        """

        PAYOR_IDENTIFICATION = "PI"
        CMS_PLAN_ID = "XV"

    entity_identifier_code: Literal["PR"]
    entity_type_qualifier: Literal["2"]
    name_first: Optional[str]
    identification_code_qualifier: IdentificationCodeQualifier


class Loop2000BHlSegment(HlSegment):
    """
    Information Receiver HL Segment
    """

    hierarchical_level_code: Literal["21"]
    hierarchical_child_code: Literal["1"]


class Loop2100BNm1Segment(Nm1Segment):
    """
    Information Receiver Name Segment
    """

    entity_identifier_code: Literal["41"]
    identification_code_qualifier: Literal["46"]


class Loop2000CHlSegment(HlSegment):
    """
    Service Provider HL Segment
    """

    hierarchical_level_code: Literal["19"]
    hierarchical_child_code: Literal["1"]


class Loop2100CNm1Segment(Nm1Segment):
    """
    Service Provider NM1 Segment
    """

    class IdentificationCodeQualifier(str, Enum):
        """
        Code values for NM108
        """

        FEDERAL_TAXPAYER_IDENTIFIER_NUMBER = "FI"
        SERVICE_PROVIDER_NUMBER = "SV"
        CMS_NATIONAL_PROVIDER_IDENTIFIER = "XX"

    entity_identifier_code: Literal["1P"]
    name_last_or_organization_name: Optional[str]
    identification_code_qualifier: IdentificationCodeQualifier


class Loop2000DHlSegment(HlSegment):
    """
    Subscriber HL Segment
    """

    hierarchical_level_code: Literal["22"]


class Loop2000DDmgSegment(DmgSegment):
    """
    Subscriber Demographics
    """

    date_time_period_format_qualifier: Literal["D8"]
    date_time_period: Optional[Union[str, datetime.date]]


class Loop2100DNm1Segment(Nm1Segment):
    """
    Subscriber Name
    """

    class IdentificationCodeQualifier(str, Enum):
        """
        Code values for NM108
        """

        EMPLOYER_IDENTIFICATION_NUMBER = "24"
        STANDARD_US_HEALTH_IDENTIFIER = "II"
        MEMBER_IDENTIFICATION_NUMBER = "MI"

    entity_identifier_code: Literal["IL"]
    entity_type_qualifier: Literal["1"]
    identification_code_qualifier: IdentificationCodeQualifier


class Loop2200DTrnSegment(TrnSegment):
    """
    Subscriber Claim Status Tracking Trace Segment
    """

    trace_type_code: Literal["1"]
    originating_company_identifier: Optional[str]
    reference_identification_2: Optional[str]


class Loop2200DRefSegment(RefSegment):
    """
    Subscriber Claim Status Tracking Trace Segment Reference Identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        PAYOR_CLAIM_NUMBER = "1K"
        BILLING_TYPE = "BLT"
        LOCATION_NUMBER = "LU"
        GROUP_NUMBER = "6P"
        PATIENT_ACCOUNT_NUMBER = "EJ"
        PHARMACY_PRESCRIPTION_NUMBER = "XZ"
        CLAIM_NUMBER = "D9"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2200DAmtSegment(AmtSegment):
    """
    Subscriber Claim Status Tracking Amount Segment
    """

    amount_qualifier_code: Literal["T3"]


class Loop2200DDtpSegment(DtpSegment):
    """
    Subscriber Claim Status Tracking Amount Segment Dates
    """

    date_time_qualifier: Literal["472"]


class Loop2210DSvcSegment(SvcSegment):
    """
    Subscriber Claim Status Service Line
    """

    line_item_provider_payment_amount: Optional[Decimal]
    original_units_of_service_count: Decimal


class Loop2210DRefSegment(RefSegment):
    """
    Subscriber Claim Status Service Line Reference Identification
    """

    reference_identification_qualifier: Literal["FJ"]


class Loop2210DDtpSegment(DtpSegment):
    """
    Subscriber Claim Status Service Line Dates
    """

    date_time_qualifier: Literal["472"]


class Loop2000EHlSegment(HlSegment):
    """
    Dependent HL Segment
    """

    hierarchical_level_code: Literal["23"]
    hierarchical_child_code: Optional[str]


class Loop2100ENm1Segment(Nm1Segment):
    """
    Dependent Name Segment
    """

    entity_identifier_code: Literal["QC"]
    entity_type_qualifier: Literal["1"]
    identification_code_qualifier: Optional[str]
    identification_code: Optional[str]
