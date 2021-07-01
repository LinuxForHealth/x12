"""
segments.py

Subclasses base segment models for use within the 270 005010X279A1 transaction set.
"""
from enum import Enum
from typing import Literal, Optional

from pydantic import Field

from x12.segments import BhtSegment, HlSegment, Nm1Segment, StSegment


class HeaderStSegment(StSegment):
    """
    Customized ST segment for 270 transaction header
    """

    transaction_set_identifier_code: Literal["270"]
    implementation_convention_reference: Literal["005010X279A1"]


class HeaderBhtSegment(BhtSegment):
    """
    Customized BHT Segment for 270 transaction header
    """

    class PurposeCode(str, Enum):
        """
        Code values for BHT02
        """

        CANCELLATION = "01"
        REQUEST = "13"

    class TransactionCode(str, Enum):
        """
        Code values for BHT06
        """

        SPEND_DOWN = "RT"

    hierarchical_structure_code: Literal["0022"]
    transaction_set_purpose_code: PurposeCode
    submitter_transactional_identifier: str = Field(min_length=1, max_length=50)
    transaction_type_code: Optional[TransactionCode]


class Loop2000AHlSegment(HlSegment):
    """
    Loop2000A HL segment adjusted for Information Source usage
    Example:
        HL*1**20*1~
    """

    class HierarchicalLevelCode(str, Enum):
        """
        Code value for HL03
        """

        INFORMATION_SOURCE = "20"

    hierarchical_id_number: Literal["1"]
    hierarchical_parent_id_number: Optional[str]
    hierarchical_level_code: HierarchicalLevelCode


class Loop2100ANm1Segment(Nm1Segment):
    """
    Loop 2100A NM1 segment adjusted for Information Source usage
    Example:
        NM1*PR*2*PAYER C*****PI*12345~
    """

    class EntityIdentifierCode(str, Enum):
        """
        Code value for NM101
        """

        THIRD_PARTY_ADMINISTRATOR = "2B"
        EMPLOYER = "36"
        GATEWAY_PROVIDER = "GP"
        PLAN_SPONSOR = "P5"
        PAYER = "PR"

    class IdentificationCodeQualifier(str, Enum):
        """
        Code value for NM108
        """

        EMPLOYER_IDENTIFICATION_NUMBER = "24"
        ELECTRONIC_TRANSMITTER_IDENTIFICATION_NUMBER = "46"
        FEDERAL_TAXPAYER_IDENTIFICATION_NUMBER = "FI"
        NATIONAL_ASSOCIATION_INSURANCE_COMMISSIONERS_ID = "NI"
        PAYOR_IDENTIFICATION = "PI"
        MEDICARE_MEDICAID_PLAN_ID = "XV"
        MEDICARE_MEDICAID_NATIONAL_PROVIDER_ID = "XX"

    entity_identifier_code: EntityIdentifierCode
    identification_code_qualifier: IdentificationCodeQualifier
    name_first: Optional[str]
    name_middle: Optional[str]
    name_suffix: Optional[str]
