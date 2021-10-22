"""
segments.py

Specialized segment models for the Health Care Claim Status Request 276 005010X212 transaction.
"""
from x12.segments import StSegment, BhtSegment, HlSegment, Nm1Segment
from typing import Literal, Optional
from enum import Enum


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
