"""
segments.py

Specialized segment models for the HealthCare Claim Professional 837 005010X222A2 transaction.
"""

from x12.segments import (
    StSegment,
    BhtSegment,
    Nm1Segment,
    PerSegment,
    HlSegment,
    PrvSegment,
    RefSegment
)
from typing import Literal, Optional
from enum import Enum
from pydantic import Field


class HeaderStSegment(StSegment):
    """
    Customized ST segment for 837 transaction header
    """

    transaction_set_identifier_code: Literal["837"]
    implementation_convention_reference: Literal["005010X222A2"]


class HeaderBhtSegment(BhtSegment):
    """
    Customized BHT segment for 837 transaction header
    """

    class PurposeCode(str, Enum):
        """
        BHT02 code values
        """

        ORIGINAL = "00"
        REISSUE = "18"

    class TransactionTypeCode(str, Enum):
        """
        BHT06 code values
        """

        SUBROGATION_DEMAND = "31"
        CHARGABLE = "CH"
        REPORTING = "RP"

    hierarchical_structure_code: Literal["0019"]
    transaction_set_purpose_code: PurposeCode
    transaction_type_code: TransactionTypeCode


class Loop1000ANm1Segment(Nm1Segment):
    """
    Submitter Name Name Segment
    """

    entity_identifier_code: Literal["41"]
    identification_code_qualifier: Literal["46"]


class Loop1000APerSegment(PerSegment):
    """
    Submitter Name Contact Segment
    """

    class CommunicationNumberQualifier1(str, Enum):
        """
        Code values for PER03
        """

        ELECTRONIC_MAIL = "EM"
        FACSIMILE = "FX"
        TELEPHONE = "TE"

    class CommunicationNumberQualifier2(str, Enum):
        """
        Code values for PER05
        """

        ELECTRONIC_MAIL = "EM"
        TELEPHONE_EXTENSION = "EX"
        FACSIMILE = "FX"
        TELEPHONE = "TE"

    communication_number_qualifier_1: CommunicationNumberQualifier1
    communication_number_qualifier_2: Optional[CommunicationNumberQualifier2]
    communication_number_qualifier_3: Optional[CommunicationNumberQualifier2]


class Loop1000BNm1Segment(Nm1Segment):
    """
    Information Receiver Name
    """

    entity_identifier_code: Literal["40"]
    identification_code_qualifier: Literal["46"]


class Loop2000AHlSegment(HlSegment):
    """
    Billing Provider Hierarchical Level
    """

    hierarchical_parent_id_number: Optional[str]
    hierarchical_level_code: Literal["20"]


class Loop2000APrvSegment(PrvSegment):
    """
    Billing Provider Speciality Information
    """

    provider_code: Literal["BI"]
    reference_identification_qualifier: Literal["PXC"]
    reference_identification: str = Field(min_length=1, max_length=50)


class Loop2010AaNm1Segment(Nm1Segment):
    """
    Billing Provider Name and Identification
    """
    entity_identifier_code: Literal["85"]
    identification_code_qualifier: Optional[Literal["XX"]]


class Loop2010AaRefSegment(RefSegment):
    """
    Billing Provider Identification Codes
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """
        EMPLOYER_IDENTIFICATION_NUMBER = "EI"
        SOCIAL_SECURITY_NUMBER = "SY"
        STATE_LICENSE_NUMBER = "0B"
        PROVIDER_UPIN_NUMBER = "1G"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2010AbNm1Segment(Nm1Segment):
    """
    Billing Provider Name and Identification
    """
    entity_identifier_code: Literal["87"]
    name_last_or_organization_name: Optional[str]
