"""
control_codes.py

Code values for X12 Control Segments
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
