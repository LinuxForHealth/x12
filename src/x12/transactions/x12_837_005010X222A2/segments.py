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
    RefSegment,
    SbrSegment,
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


class Loop2010AcNm1Segment(Nm1Segment):
    """
    Pay to Plan Name and Identification
    """

    class IdentificationCodeQualifier(str, Enum):
        """
        Code values for NM108
        """

        PAYOR_IDENTIFICATION = "PI"
        CMS_PLAN_ID = "XV"

    entity_identifier_code: Literal["PE"]
    entity_type_qualifier: Literal["2"]
    name_last_or_organization_name: Optional[str]
    identification_code_qualifier: IdentificationCodeQualifier


class Loop2010AcRefSegment(RefSegment):
    """
    Pay to Plan Identification Codes
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        PAYER_IDENTIFICATION_NUMBER = "2u"
        CLAIM_OFFICE_NUMBER = "FY"
        NAIC_CODE = "NF"
        EMPLOYERS_IDENTIFICATION_NUMBER = "EI"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2000BHlSegment(HlSegment):
    """
    Subscriber Hierarchy Segment
    """

    hierarchical_level_code: Literal["22"]


class Loop2000BSbrSegment(SbrSegment):
    """
    Subscriber Information Segment

    TODO: validation rules
    """

    class PayerResponsibilityCode(str, Enum):
        """
        SBR01 code values
        """

        PAYER_RESPONSIBILITY_FOUR = "A"
        PAYER_RESPONSIBILITY_FIVE = "B"
        PAYER_RESPONSIBILITY_SIX = "C"
        PAYER_RESPONSIBILITY_SEVEN = "D"
        PAYER_RESPONSIBILITY_EIGHT = "E"
        PAYER_RESPONSIBILITY_NINE = "F"
        PAYER_RESPONSIBILITY_TEN = "G"
        PRIMARY = "P"
        SECONDARY = "S"
        TERTIARY = "T"
        UNKNOWN = "U"

    class InsuranceTypeCode(str, Enum):
        """
        SBR05 code values
        """

        MEDICARE_SECONDARY_WORKING = "12"
        MEDICARE_SECONDARY_END_STAGE_RENAL = "13"
        MEDICARE_SECONDARY_AUTO_PRIMARY = "14"
        MEDICARE_SECONDARY_WORKERS_COMPENSATION = "15"
        MEDICARE_SECONDARY_PUBLIC_HEALTH_SERVICE = "16"
        MEDICARE_SECONDARY_BLACK_LUNG = "41"
        MEDICARE_SECONDARY_VETERANS_ADMINISTRATION = "42"
        MEDICARE_SECONDARY_DISABLED_BENEFICIARY = "43"
        MEDICARE_SECONDARY_LIABILITY_PRIMARY = "47"

    class ClaimFilingIndicatorCode(str, Enum):
        """
        SBR09 code values
        """

        OTHER_NON_FEDERAL_PROGRAMS = "11"
        PREFERRED_PROVIDER_ORGANIZATION = "12"
        POINT_OF_SERVICE = "13"
        EXCLUSIVE_PROVIDER_ORGANIZATION = "14"
        INDEMNITY_INSURANCE = "15"
        HEALTH_MAINTENANCE_ORGANIZATION_MEDICARE_RISK = "16"
        DENTAL_MAINTENANCE_ORGANIZATION = "17"
        AUTOMOBILE_MEDICAL = "AM"
        BLUE_CROSS_BLUE_SHIELD = "BL"
        CHAMPUS = "CH"
        COMMERICIAL_INSURANCE_COMPANY = "CI"
        DISABILITY = "DS"
        FEDERAL_EMPLOYEES_PROGRAM = "FI"
        HEALTH_MAINTENANCE_ORGANIZATION = "HM"
        LIABILITY_MEDICAL = "LM"
        MEDICARE_PART_A = "MA"
        MEDICARE_PART_B = "MB"
        MEDICAID = "MC"
        OTHER_FEDERAL_PROGRAM = "OF"
        TITLE_V = "TV"
        VETERANS_AFFAIR_PLAN = "VA"
        WORKERS_COMPENSATION_HEALTH_CLAIM = "WC"
        MUTUALLY_DEFINED = "ZZ"

    payer_responsibility_code: PayerResponsibilityCode
    individual_relationship_code: Optional[Literal["18"]]
    insurance_type_code: Optional[InsuranceTypeCode]


class Loop2010BaNm1Segment(Nm1Segment):
    """
    Subscriber Name Segment
    """

    entity_identifier_code: Literal["IL"]


class Loop2010BaRefSegment(RefSegment):
    """
    Subscriber Name Reference Identification
    """
    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """
        SOCIAL_SECURITY_NUMBER = "SY"
        AGENCY_CLAIM_NUMBER = "Y4"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2010BaPerSegment(PerSegment):
    """
    Subscriber Name Contact Information
    """

    communication_number_qualifier_1: Literal["TE"]
    communication_number_qualifier_2: Optional[Literal["EX"]]
