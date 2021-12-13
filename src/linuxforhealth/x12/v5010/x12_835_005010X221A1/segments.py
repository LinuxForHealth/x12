"""
segments.py

Specialized segment models for the Health Care Claim Payment 835 005010X221A1 transaction set model.
"""
from linuxforhealth.x12.v5010.segments import (
    StSegment,
    TrnSegment,
    CurSegment,
    RefSegment,
    DtmSegment,
    PerSegment,
    N1Segment,
    CasSegment,
    AmtSegment,
    QtySegment,
    LqSegment,
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


class Loop2100CasSegment(CasSegment):
    """
    Claim Payment Information CAS segment
    """

    class ClaimAdjustmentGroupCode(str, Enum):
        """
        Code values for CAS01
        """

        CONTRACTUAL_OBLIGATIONS = "CO"
        OTHER_ADJUSTMENTS = "OA"
        PAYER_INITIATED_REDUCTIONS = "PI"
        PATIENT_RESPONSIBILITY = "PR"

    adjustment_group_code: ClaimAdjustmentGroupCode


class Loop2100RefSegment(RefSegment):
    """
    Claim Payment Reference Identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        GROUP_POLICY_NUMBER = "1L"
        MEMBER_IDENTIFICATION_NUMBER = "1W"
        EMPLOYEE_IDENTIFICATION_NUMBER = "28"
        GROUP_NUMBER = "6P"
        REPRICED_CLAIM_REFERENCE_NUMBER = "9A"
        ADJUSTED_REPRICED_CLAIM_REFERENCE_NUMBER = "9C"
        AUTHORIZATION_NUMBER = "BB"
        CLASS_OF_CONTRACT_CODE = "CE"
        MEDICAL_RECORD_IDENTIFICATION_NUMBER = "EA"
        ORIGINAL_REFERENCE_NUMBER = "F8"
        PRIOR_AUTHORIZATION_NUMBER = "G1"
        PREDETERMINATION_BENEFITS_IDENTIFICATION_NUMBER = "G3"
        INSURANCE_POLICY_NUMBER = "IG"
        SOCIAL_SECURITY_NUMBER = "SY"
        STATE_LICENSE_NUMBER = "0B"
        BLUE_CROSS_PROVIDER_NUMBER = "1A"
        BLUE_SHIELD_PROVIDER_NUMBER = "1B"
        MEDICARE_PROVIDER_NUMBER = "1C"
        MEDICAID_PROVIDER_NUMBER = "1D"
        PROVIDER_UPIN_NUMBER = "1G"
        CHAMPUS_IDENTIFICATION_NUMBER = "1H"
        FACILITY_ID_NUMBER = "1J"
        NATIONAL_COUNCIL_PRESCRIPTION_PHARMACY_NUMBER = "D3"
        PROVIDER_COMMERCIAL_NUMBER = "G2"
        LOCATION_NUMBER = "LU"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2100DtmSegment(DtmSegment):
    """
    Claim Payment Information Date Time Reference
    """

    class DateTimeQualifier(str, Enum):
        """
        DTM01 code values
        """

        CLAIM_STATEMENT_PERIOD_START = "232"
        CLAIM_STATEMENT_PERIOD_STOP = "233"
        EXPIRATION = "036"
        RECEIVED = "050"

    date_time_qualifier: DateTimeQualifier


class Loop2100PerSegment(PerSegment):
    """
    Claim Payment Contact Information
    """

    contact_function_code: Literal["CX"]


class Loop2100AmtSegment(AmtSegment):
    """
    Claim Payment Amounts
    """

    class AmountQualifierCode(str, Enum):
        """
        Code values for AMT01
        """

        COVERAGE_AMOUNT = "AU"
        DISCOUNT_AMOUNT = "D8"
        PER_DAY_LIMIT = "DY"
        PATIENT_AMOUNT_PAID = "F5"
        INTEREST = "I"
        NEGATIVE_LEDGER_BALANCE = "NL"
        TAX = "T"
        TOTAL_CLAIM_BEFORE_TAXES = "T2"
        FEDERAL_MANDATE_CATEGORY_1 = "ZK"
        FEDERAL_MANDATE_CATEGORY_2 = "ZL"
        FEDERAL_MANDATE_CATEGORY_3 = "ZM"
        FEDERAL_MANDATE_CATEGORY_4 = "ZN"
        FEDERAL_MANDATE_CATEGORY_5 = "ZO"

    amount_qualifier_code: AmountQualifierCode


class Loop2100QtySegment(QtySegment):
    """
    Payment Information Quantity
    """

    class QuantityQualifier(str, Enum):
        """
        Code values for QTY01
        """

        COVERED_ACTUAL = "CA"
        COINSURED_ACTUAL = "CD"
        LIFE_TERM_RESERVE_ACTUAL = "LA"
        LIFE_TERM_RESERVE_ESTIMATED = "LE"
        NONCOVERED_ESTIMATED = "NE"
        NOT_REPLACED_BLOOD_UNITS = "NR"
        OUTLIER_DAYS = "OU"
        PRESCRIPTION = "PS"
        VISITS = "VS"
        FEDERAL_PAYMENT_MANDATE_CATEGORY_1 = "ZK"
        FEDERAL_PAYMENT_MANDATE_CATEGORY_2 = "ZL"
        FEDERAL_PAYMENT_MANDATE_CATEGORY_3 = "ZM"
        FEDERAL_PAYMENT_MANDATE_CATEGORY_4 = "ZN"
        FEDERAL_PAYMENT_MANDATE_CATEGORY_5 = "ZO"

    quantity_qualifier: QuantityQualifier


class Loop2110DtmSegment(DtmSegment):
    """
    Service Line Payment Information Date
    """

    class DateTimeQualifier(str, Enum):
        """
        Code values for DTM01
        """

        SERVICE_PERIOD_START = "150"
        SERVICE_PERIOD_END = "151"
        SERVICE = "472"

    date_time_qualifier: DateTimeQualifier


class Loop2110CasSegment(CasSegment):
    """
    Service Line Payment Information Adjustments
    """

    class ClaimAdjustmentGroupCode(str, Enum):
        """
        Code values for CAS01
        """

        CONTRACTURAL_OBLIGATIONS = "CO"
        OTHER_ADJUSTMENTS = "OA"
        PAYOR_INITIATED_REDUCTIONS = "PI"
        PATIENT_RESPONSIBILITY = "PR"

    adjustment_group_code: ClaimAdjustmentGroupCode


class Loop2110RefSegment(RefSegment):
    """
    Service Line Payment Information Reference Identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        AMBULATORY_PATIENT_GROUP_NUMBER = "1S"
        AMBULATORY_PAYMENT_CLASSIFICATION = "APC"
        AUTHORIZATION_NUMBER = "BB"
        ATTACHMENT_CODE = "E9"
        PRIOR_AUTHORIZATION_NUMBER = "G1"
        PREDETERMINATION_OF_BENEFITS_NUMBER = "G3"
        LOCATION_NUMBER = "LU"
        RATE_CODE_NUMBER = "RB"
        PROVIDER_CONTROL_NUMBER = "6R"
        STATE_LICENSE_NUMBER = "0B"
        BLUE_CROSS_PROVIDER_NUMBER = "1A"
        BLUE_SHIELD_PROVIDER_NUMBER = "1B"
        MEDICARE_PROVIDER_NUMBER = "1C"
        MEDICAID_PROVIDER_NUMBER = "1D"
        PROVIDER_UPIN_NUMBER = "1G"
        CHAMPUS_IDENTIFICATION_NUMBER = "1H"
        FACILITY_ID_NUMBER = "1J"
        NATIONAL_COUNCIL_PRESCRIPTION_PHARMACY_NUMBER = "D3"
        PROVIDER_COMMERCIAL_NUMBER = "G2"
        POLICY_FORM_IDENTIFYING_NUMBER = "0K"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2110AmtSegment(AmtSegment):
    """
    Service Line Payment Information Amount
    """

    class AmountQualifierCode(str, Enum):
        """
        Code values for AMT01
        """

        ALLOWED_ACTUAL = "B6"
        DEDUCTION_AMOUNT = "KH"
        TAX = "T"
        TOTAL_CLAIM_BEFORE_TAXES = "T2"
        FEDERAL_PAYMENT_MANDATE_CATEGORY_1 = "ZK"
        FEDERAL_PAYMENT_MANDATE_CATEGORY_2 = "ZL"
        FEDERAL_PAYMENT_MANDATE_CATEGORY_3 = "ZM"
        FEDERAL_PAYMENT_MANDATE_CATEGORY_4 = "ZN"
        FEDERAL_PAYMENT_MANDATE_CATEGORY_5 = "ZO"

    amount_qualifier_code: AmountQualifierCode


class Loop2110QtySegment(QtySegment):
    """
    Service Line Payment Information Quantity
    """

    class QuantityQualifier(str, Enum):
        """
        Code values for QTY01
        """

        FEDERAL_PAYMENT_MANDATE_CATEGORY_1 = "ZK"
        FEDERAL_PAYMENT_MANDATE_CATEGORY_2 = "ZL"
        FEDERAL_PAYMENT_MANDATE_CATEGORY_3 = "ZM"
        FEDERAL_PAYMENT_MANDATE_CATEGORY_4 = "ZN"
        FEDERAL_PAYMENT_MANDATE_CATEGORY_5 = "ZO"

    quantity_qualifier: QuantityQualifier


class Loop2110LqSegment(LqSegment):
    """
    Service Line Payment Information Health Care Remark Codes
    """

    class CodeListQualifierCodes(str, Enum):
        """
        Code values for LQ01
        """

        CLAIM_PAYMENT_REMARK_CODES = "HE"
        NATIONAL_COUNCIL_PRESCRIPTION_DRUG_REJECT_PAYMENT_CODES = "RX"

    code_list_qualifier_code: CodeListQualifierCodes
