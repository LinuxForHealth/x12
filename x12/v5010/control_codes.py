"""
control_codes.py

Code values for ASC X12 Control Segments
"""
from enum import Enum


class AuthorizationInformationQualifier(str, Enum):
    """
    ISA01 Code Values
    """

    NO_AUTHORIZATION_PRESENT = "00"
    ADDITIONAL_DATA_IDENTIFICATION = "03"


class SecurityInformationQualifier(str, Enum):
    """
    ISA03 Code Values
    """

    NO_SECURITY_INFO_PRESENT = "00"
    PASSWORD = "01"


class InterchangeIdQualifier(str, Enum):
    """
    ISA05 and ISA07 Code Values
    """

    DUNS = "01"
    DUNS_PLUS_SUFFIX = "14"
    HEALTH_INDUSTRY_NUMBER = "20"
    CARRIER_ID_NUMBER = "27"
    FISCAL_ID_NUMBER = "28"
    MEDICARE_PROVIDER_ID = "29"
    US_FEDERAL_TAX_ID = "30"
    NAIC_CODE = "33"
    MUTUALLY_DEFINED = "ZZ"


class InterchangeControlVersion(str, Enum):
    """
    ISA12 Code Values
    """

    VERSION = "00501"


class AcknowledgmentRequested(str, Enum):
    """
    ISA14 Code Values
    """

    NO_ACKNOWLEDGMENT_REQUESTED = "0"
    ACKNOWLEDGMENT_REQUESTED = "1"


class InterchangeUsage(str, Enum):
    """
    ISA15 code values
    """

    PRODUCTION = "P"
    TEST = "T"


class FunctionalIdCode(str, Enum):
    """
    GS01 code values
    """

    CLAIM_STATUS_REQUEST = "HR"  # 276
    CLAIM_STATUS_NOTIFICATION = "HN"  # 277
    SERVICES_REVIEW = "HI"  # 278
    PAYMENT_ORDER = "RA"  # 820
    BENEFIT_ENROLLMENT = "BE"  # 834
    CLAIM_PAYMENT = "HP"  # 835
    CLAIM = "HC"  # 837 (Professional, Institutional, and Dental)
    ELIGIBILITY_INFORMATION = "HB"  # 271
    ELIGIBILITY_INQUIRY = "HS"  # 270


class TransactionSetCode(str, Enum):
    """
    ST01 code values
    """
    BENEFIT_ENROLLMENT = "834"
    CLAIM_PAYMENT = "835"
    CLAIM_STATUS_REQUEST = "276"
    CLAIM_STATUS_NOTIFICATION = "277"
    DENTAL_CLAIM = "837"
    ELIGIBILITY_INFORMATION = "271"
    ELIGIBILITY_INQUIRY = "270"
    INSTITUTIONAL_CLAIM = "837"
    PAYMENT_ORDER = "820"
    PROFESSIONAL_CLAIM = "837"
    SERVICES_REVIEW = "278"


class ImplementationReference(str, Enum):
    """
    ST03 code values
    """
    BENEFIT_ENROLLMENT = "005010X220A1"
    CLAIM_PAYMENT = "005010X221A1"
    CLAIM_STATUS_REQUEST = "005010X212"
    CLAIM_STATUS_NOTIFICATION = "005010X212"
    DENTAL_CLAIM = "005010X224A3"
    ELIGIBILITY_INQUIRY = "005010X279A1"
    ELIGIBILITY_INFORMATION = "005010X279A1"
    INSTITUTIONAL_CLAIM = "005010X223A3"
    PAYMENT_ORDER = "005010X218"
    PROFESSIONAL_CLAIM = "005010X222A2"
    SERVICES_REVIEW = "005010X217"
