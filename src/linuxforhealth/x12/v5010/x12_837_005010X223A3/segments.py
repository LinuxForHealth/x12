"""
segments.py

Specialized segment models for the HealthCare Claim Institutional 837 005010X223A3 transaction.
"""

from linuxforhealth.x12.v5010.segments import (
    StSegment,
    BhtSegment,
    Nm1Segment,
    PerSegment,
    HlSegment,
    PrvSegment,
    RefSegment,
    SbrSegment,
    DtpSegment,
    Cn1Segment,
    AmtSegment,
    NteSegment,
    CrcSegment,
    PatSegment,
    HcpSegment,
    PwkSegment,
)
from typing import Literal, Optional, Dict, Union
from enum import Enum
from pydantic import Field, root_validator
import datetime


class HeaderStSegment(StSegment):
    """
    Customized ST segment for 837 transaction header
    """

    transaction_set_identifier_code: Literal["837"]
    implementation_convention_reference: Literal["005010X223A3"]


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
    identification_code: str = Field(min_length=2, max_length=80)


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
    entity_type_qualifier: Literal["2"]
    identification_code_qualifier: Literal["46"]


class Loop2000AHlSegment(HlSegment):
    """
    Billing Provider Hierarchical Level
    """

    hierarchical_parent_id_number: Optional[str]
    hierarchical_level_code: Literal["20"]
    hierarchical_child_code: Literal["1"]


class Loop2000APrvSegment(PrvSegment):
    """
    Billing Provider Speciality Information
    """

    provider_code: Literal["BI"]
    reference_identification_qualifier: Literal["PXC"]
    reference_identification: str = Field(min_length=1, max_length=50)


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
        PAYER_RESPONSIBILITY_ELEVEN = "H"
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


class Loop2000CHlSegment(HlSegment):
    """
    The HL segment for Loop 2000C (Patient)
    """

    hierarchical_level_code: Literal["23"]
    hierarchical_child_code: Literal["0"]


class Loop2000CPatSegment(PatSegment):
    """
    The PAT, patient, segment for Loop2000C
    """

    class IndividualRelationshipCode(str, Enum):
        """
        Code values for PAT01
        """

        SPOUSE = "01"
        CHILD = "19"
        EMPLOYEE = "20"
        UNKNOWN = "21"
        ORGAN_DONOR = "39"
        CADAVER_DONOR = "40"
        LIFE_PARTNER = "53"
        OTHER_RELATIONSHIP = "G8"

    individual_relationship_code: IndividualRelationshipCode


class Loop2010AaNm1Segment(Nm1Segment):
    """
    Billing Provider Name and Identification
    """

    entity_identifier_code: Literal["85"]
    entity_type_qualifier: Literal["2"]
    identification_code_qualifier: Optional[Literal["XX"]]


class Loop2010AaRefSegment(RefSegment):
    """
    Billing Provider Identification Codes
    """

    reference_identification_qualifier: Literal["EI"]


class Loop2010AaPerSegment(PerSegment):
    """
    Billing Provider Contact Information
    """

    class CommunicationNumberQualifier(str, Enum):
        ELECTRONIC_MAIL = "EM"
        TELEPHONE_EXTENSION = "EX"
        FACSIMILE = "FX"
        TELEPHONE = "TE"

    communication_number_qualifier_1: CommunicationNumberQualifier
    communication_number_qualifier_2: Optional[CommunicationNumberQualifier]
    communication_number_qualifier_3: Optional[CommunicationNumberQualifier]


class Loop2010AbNm1Segment(Nm1Segment):
    """
    Billing Provider Name and Identification
    """

    entity_identifier_code: Literal["87"]
    entity_type_qualifier: Literal["2"]
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
    identification_code_qualifier: IdentificationCodeQualifier


class Loop2010AcRefSegment(RefSegment):
    """
    Pay to Plan Identification Codes
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        PAYER_IDENTIFICATION_NUMBER = "2U"
        CLAIM_OFFICE_NUMBER = "FY"
        NAIC_CODE = "NF"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2010BaNm1Segment(Nm1Segment):
    """
    Subscriber Name Segment
    """

    class IdentificationCodeQualifier(str, Enum):
        """
        Code values for NM108
        """

        STANDARD_HEALTH_ID_US = "II"
        MEMBER_IDENTIFICATION_NUMBER = "MI"

    entity_identifier_code: Literal["IL"]
    identification_code_qualifier: Optional[IdentificationCodeQualifier]


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


class Loop2010BbNm1Segment(Nm1Segment):
    """
    Subscriber Name Segment
    """

    class IdentificationCodeQualifier(str, Enum):
        """
        Code values for NM108
        """

        PAYOR_IDENTIFICATION = "PI"
        CMS_PLAN_ID = "XV"

    entity_identifier_code: Literal["PR"]
    entity_type_qualifier: Literal["2"]
    identification_code_qualifier: IdentificationCodeQualifier
    identification_code: str = Field(min_length=2, max_length=80)


class Loop2010BbRefSegment(RefSegment):
    """
    Payer Name Reference Identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        PAYER_IDENTIFICATION_NUMBER = "2U"
        EMPLOYERS_IDENTIFICATION_NUMBER = "EI"
        CLAIM_OFFICER_NUMBER = "FY"
        NAIC_CODE = "NF"
        PROVIDER_CONTROL_NUMBER = "G2"
        LOCATION_NUMBER = "LU"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2010CaNm1Segment(Nm1Segment):
    """
    Loop2010CA NM1 segment for Patient
    """

    entity_identifier_code: Literal["QC"]
    entity_type_qualifier: Literal["1"]


class Loop2010CaRefSegment(RefSegment):
    """
    Loop 2010CA (Patient Name) REF Segment
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        AGENCY_CLAIM_NUMBER = "Y4"
        MEMBER_IDENTIFICATION_NUMBER = "1W"
        SOCIAL_SECURITY_NUMBER = "SY"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2300DtpSegment(DtpSegment):
    """
    Claim information DTP segments
    """

    class DateTimeQualifier(str, Enum):
        """
        Code values for DTP01
        """

        DISCHARGE = "096"
        STATEMENT = "434"
        ADMISSION = "435"
        RECEIVED = "050"

    class DateTimePeriodFormatQualifier(str, Enum):
        """
        Code values for DTP02
        """

        TIME = "TM"
        DATE = "D8"
        DATE_AND_TIME = "DT"
        DATE_RANGE = "RD8"

    date_time_qualifier: DateTimeQualifier
    date_time_period_format_qualifier: DateTimePeriodFormatQualifier
    date_time_period: Union[str, datetime.datetime, datetime.date]

    @root_validator
    def validate_disability_dates(cls, values: Dict):
        """
        Validates that a date range qualifier is used for disability dates.

        :param values: The model's values
        :return: The model's values
        """
        date_qualifier = values.get("date_time_qualifier")
        period_qualifier = values.get("date_time_period_format_qualifier")

        if date_qualifier == "314" and period_qualifier != "RD8":
            raise ValueError(
                "RD8 Date Time Period is required for Disability Dates (314)"
            )
        return values


class Loop2300PwkSegment(PwkSegment):
    """
    Claim information paperwork segment
    """

    class AttachmentReportTypeCode(str, Enum):
        """
        PWK01 code values
        """

        REPORT_JUSTIFYING_TREATMENT_BEYOND_UTILIZATION_GUIDELINES = "03"
        DRUGS_ADMINISTERED = "04"
        TREATMENT_DIAGNOSIS = "05"
        INITIAL_ASSESSMENT = "06"
        FUNCTIONAL_GOALS = "07"
        PLAN_OF_TREATMENT = "08"
        PROGRESS_REPORT = "09"
        CONTINUED_TREATMENT = "10"
        CHEMICAL_ANALYSIS = "11"
        CERTIFIED_TEST_REPORT = "13"
        JUSTIFICATION_FOR_ADMISSION = "15"
        RECOVERY_PLAN = "21"
        ALLERGIES_SENSITIVITIES_DOCUMENT = "A3"
        AUTOPSY_REPORT = "A4"
        AMBULANCE_CERTIFICATION = "AM"
        ADMISSION_SUMMARY = "AS"
        PRESCRIPTION = "B2"
        PHYSICIAN_ORDER = "B3"
        REFERRAL_FORM = "B4"
        BENCHMARK_TESTING_RESULTS = "BR"
        BASELINE = "BS"
        BLANKET_TESTING_RESULTS = "BT"
        CHIROPRACTIC_JUSTIFICATION = "CB"
        CONSENT_FORM = "CK"
        CERTIFICATION = "CT"
        DRUG_PROFILE_DOCUMENT = "D2"
        DENTAL_MODELS = "DA"
        DURABLE_MEDICAL_EQUIPMENT_PRESCRIPTION = "DB"
        DIAGNOSTIC_REPORT = "DG"
        DISCHARGE_MONITORING_REPORT = "DJ"
        DISCHARGE_SUMMARY = "DS"
        EXPLANATION_OF_BENEFITS = "EB"
        HEALTH_CERTIFICATE = "HC"
        HEALTH_CLINIC_RECORDS = "HR"
        IMMUNIZATION_RECORD = "I5"
        STATE_SCHOOL_IMMUNIZATION_RECORDS = "IR"
        LABORATORY_RESULTS = "LA"
        MEDICAL_RECORD_ATTACHMENT = "M1"
        MODELS = "MT"
        NURSING_NOTES = "NN"
        OPERATIVE_NOTE = "OB"
        OXYGEN_CONTENT_AVERAGING_REPORT = "OC"
        ORDERS_AND_TREATMENTS_DOCUMENT = "OD"
        OBJECTIVE_PHYSICAL_EXAMINATION = "OE"
        OXYGEN_THERAPY_CERTIFICATION = "OX"
        SUPPORT_DATA_FOR_CLAIM = "OZ"
        PATHOLOGY_REPORT = "P4"
        PATIENT_MEDICAL_HISTORY_DOCUMENT = "P5"
        PARENTAL_OR_ENTERAL_CERTIFICATION = "PE"
        PHYSICAL_THERAPY_NOTES = "PN"
        PROSTHETICS_OR_ORTHOTIC_CERTIFICATION = "PO"
        PARAMEDICAL_RESULTS = "PQ"
        PHYSICIANS_REPORT = "PY"
        PHYSICAL_THERAPY_CERTIFICATION = "PZ"
        RADIOLOGY_FILMS = "RB"
        RADIOLOGY_REPORTS = "RR"
        REPORT_OF_TESTS_AND_ANALYSIS_REPORT = "RT"
        RENEWABLE_OXYGEN_CONTENT_AVERAGING_REPORT = "RX"
        SYMPTOMS_DOCUMENT = "SG"
        DEATH_NOTIFICATION = "V5"
        PHOTOGRAPHS = "XP"

    class AttachmentTransmissionCode(str, Enum):
        """
        Code values for PWK02
        """

        AVAILABLE_ON_REQUEST_PROVIDER_SITE = "AA"
        BY_MAIL = "BM"
        ELECTRONICALLY_ONLY = "EL"
        EMAIL = "EM"
        FILE_TRANSFER = "FT"
        BY_FAX = "FX"

    report_type_code: AttachmentReportTypeCode
    report_transmission_code: AttachmentTransmissionCode


class Loop2300Cn1Segment(Cn1Segment):
    """
    Claim information contract information
    """

    class ContractTypeCode(str, Enum):
        """
        Code values for CN101
        """

        DIAGNOSIS_RELATED_GROUP = "01"
        PER_DIEM = "02"
        VARIABLE_PER_DIEM = "03"
        FIAT = "04"
        CAPITATED = "05"
        PERCENT = "06"
        OTHER = "09"

    contract_type_code: ContractTypeCode


class Loop2300AmtSegment(AmtSegment):
    """
    Monetary Amount
    """

    amount_qualifier_code: Literal["F3"]


class Loop2300RefSegment(RefSegment):
    """
    Claim information reference identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        SPECIAL_PAYMENT_REFERENCE_NUMBER = "4N"
        REFERRAL_NUMBER = "9F"
        PRIOR_AUTHORIZATION_NUMBER = "G1"
        ORIGINAL_REFERENCE_NUMBER = "F8"
        REPRICED_CLAIM_REFERENCE_NUMBER = "9A"
        ADJUSTED_REPRICED_CLAIM_REFERENCE_NUMBER = "9C"
        QUALIFIED_PRODUCTS_LIST = "LX"
        CLAIM_NUMBER = "D9"
        LOCATION_NUMBER = "LU"
        MEDICAL_RECORD_IDENTIFICATION_NUMBER = "EA"
        PROJECT_CODE = "P4"
        PEER_REVIEW_ORG_APPROVAL_NUMBER = "G4"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2300NteSegment(NteSegment):
    """
    Claim information note segment
    """

    class NoteReferenceCode(str, Enum):
        """
        Code values for NTE01
        """

        ALLERGIES = "ALG"
        GOALS_REHAB_POTENTIAL_DISCHARGE_PLANS = "DCP"
        DIAGNOSIS_DESCRIPTION = "DGN"
        DURABLE_MEDICAL_EQUIPMENT_SUPPLIES = "DME"
        MEDICATIONS = "MED"
        NUTRITIONAL_REQUIREMENTS = "NTR"
        ORDERS_FOR_DISCIPLINES_AND_TREATMENTS = "ODT"
        FUNCTIONAL_LIMITATIONS_REASON_HOMEBOUND = "RHB"
        REASONS_PATIENT_LEAVES_HOME = "RLH"
        TIMES_REASONS_PATIENT_NOT_AT_HOME = "RNH"
        UNUSUAL_HOME_SOCIAL_ENV_OR_BOTH = "SET"
        SAFETY_MEASURES = "SFM"
        SUPPLEMENTARY_PLAN_OF_TREATMENT = "SPT"
        UPDATED_INFORMATION = "UPI"

    note_reference_code: NoteReferenceCode


class Loop2300CrcEpSdtRefferal(CrcSegment):
    """
    Claim Information - Homebound indicator
    """

    class YesNoResponseCode(str, Enum):
        """
        Code values for CRC02
        """

        NO = "N"
        YES = "Y"

    class ConditionsIndicator(str, Enum):
        """
        Code values for CRC03 - CRC07
        """

        AVAILABLE_NOT_USED = "AV"
        NOT_USED = "NU"
        UNDER_TREATMENT = "S2"
        NEW_SERVICES_REQUESTED = "ST"

    code_category: Literal["ZZ"]
    certification_condition_indicator: YesNoResponseCode
    condition_code_1: ConditionsIndicator
    condition_code_2: Optional[ConditionsIndicator]
    condition_code_3: Optional[ConditionsIndicator]
    condition_code_4: Optional[ConditionsIndicator]
    condition_code_5: Optional[ConditionsIndicator]


class Loop2300HcpSegment(HcpSegment):
    class PricingMethodologyCodes(str, Enum):
        """
        Code values for HCP01
        """

        ZERO_PRICING_NOT_COVERED = "00"
        PRICED_AS_BILLED_100_PERCENT = "01"
        PRICED_AT_STANDARD_FEE_SCHEDULE = "02"
        PRICED_AT_CONTRACTUAL_PERCENTAGE = "03"
        BUNDLED_PRICING = "04"
        PEER_REVIEW_PRICING = "05"
        PER_DIEM_PRICING = "06"
        FLAT_RATE_PRICING = "07"
        COMBINATION_PRICING = "08"
        MATERNITY_PRICING = "09"
        OTHER_PRICING = "10"
        LOWER_OF_COST = "11"
        RATIO_OF_COST = "12"
        COST_REIMBURSED = "13"
        ADJUSTMENT_PRICING = "14"

    class MeasurementCodes(str, Enum):
        """
        Code values for HCP11
        """

        DAYS = "DA"
        UNIT = "UN"

    pricing_methodology: PricingMethodologyCodes
    unit_basis_measurement_code: Optional[MeasurementCodes]


class Loop2310ANm1Segment(Nm1Segment):
    """
    Claim Attending Provider Name
    """

    entity_identifier_code: Literal["71"]
    entity_type_qualifier: Literal["1"]
    identification_code_qualifier: Optional[Literal["XX"]]


class Loop2310APrvSegment(PrvSegment):
    """
    Attending Provider Speciality Information
    """

    provider_code: Literal["AT"]
    reference_identification_qualifier: Literal["PXC"]
    reference_identification: str = Field(min_length=1, max_length=50)


class Loop2310ARefSegment(RefSegment):
    """
    Claim Referring Provider Reference Identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        STATE_LICENSE_NUMBER = "0B"
        PROVIDER_UPIN_NUMBER = "1G"
        PROVIDER_COMMERCIAL_NUMBER = "G2"
        LOCATION_NUMBER = "LU"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2310BNm1Segment(Nm1Segment):
    """
    Claim Operating Physician Name
    """

    entity_identifier_code: Literal["72"]
    entity_type_qualifier: Literal["1"]
    identification_code_qualifier: Literal["XX"]


class Loop2310BRefSegment(RefSegment):
    """
    Claim ROperating Physician Reference Identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        STATE_LICENSE_NUMBER = "0B"
        PROVIDER_UPIN_NUMBER = "1G"
        PROVIDER_COMMERCIAL_NUMBER = "G2"
        LOCATION_NUMBER = "LU"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2310CNm1Segment(Nm1Segment):
    """
    Claim Other Operating Physician Name
    """

    entity_identifier_code: Literal["ZZ"]
    entity_type_qualifier: Literal["1"]
    identification_code_qualifier: Optional[Literal["XX"]]


class Loop2310CRefSegment(RefSegment):
    """
    Claim Service Facility Location Reference Identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        STATE_LICENSE_NUMBER = "0B"
        PROVIDER_UPIN_NUMBER = "1G"
        PROVIDER_COMMERCIAL_NUMBER = "G2"
        LOCATION_NUMBER = "LU"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2310DNm1Segment(Nm1Segment):
    """
    Claim Rendering Provider Name
    """

    entity_identifier_code: Literal["82"]
    entity_type_qualifier: Literal["1"]
    identification_code_qualifier: Optional[Literal["XX"]]


class Loop2310DRefSegment(Nm1Segment):
    """
    Claim Rendering Provider Reference Identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        STATE_LICENSE_NUMBER = "0B"
        PROVIDER_UPIN_NUMBER = "1G"
        PROVIDER_COMMERCIAL_NUMBER = "G2"
        LOCATION_NUMBER = "LU"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2310ENm1Segment(Nm1Segment):
    """
    Service Facility Location Name
    """

    entity_identifier_code: Literal["77"]
    entity_type_qualifier: Literal["2"]
    name_last_or_organization_name: Optional[str]
    identification_code_qualifier: Optional[Literal["XX"]]


class Loop2310ERefSegment(RefSegment):
    """
    Service Facility Location Reference Identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        STATE_LICENSE_NUMBER = "0B"
        PROVIDER_COMMERCIAL_NUMBER = "G2"
        LOCATION_NUMBER = "LU"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2310FNm1Segment(Nm1Segment):
    """
    Claim ambulance pickup location
    """

    entity_identifier_code: Literal["DN"]
    entity_type_qualifier: Literal["1"]
    identification_code_qualifier: Optional[Literal["XX"]]


class Loop2310FRefSegment(RefSegment):
    """
    Referring Provider Reference Identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        STATE_LICENSE_NUMBER = "0B"
        PROVIDER_UPIN_NUMBER = "1G"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2320SbrSegment(SbrSegment):
    """
    Claim Other Subscriber
    """

    class PayerResponsibilityCode(str, Enum):
        """
        Code values for SBR01
        """

        PAYER_RESPONSIBILITY_FOUR = "A"
        PAYER_RESPONSIBILITY_FIVE = "B"
        PAYER_RESPONSIBILITY_SIX = "C"
        PAYER_RESPONSIBILITY_SEVEN = "D"
        PAYER_RESPONSIBILITY_EIGHT = "E"
        PAYER_RESPONSIBILITY_NINE = "F"
        PAYER_RESPONSIBILITY_TEN = "G"
        PAYER_RESPONSIBILITY_ELEVEN = "H"
        PAYER_RESPONSIBILITY_PRIMARY = "P"
        PAYER_RESPONSIBILITY_SECONDARY = "S"
        PAYER_RESPONSIBILITY_TERTIARY = "T"
        PAYER_RESPONSIBILITY_UNKNOWN = "U"

    class IndividualRelationshipCode(str, Enum):
        """
        Code values for SBR02
        """

        SPOUSE = "01"
        SELF = "18"
        CHILD = "19"
        EMPLOYEE = "20"
        UNKNOWN = "21"
        ORGAN_DONOR = "39"
        CADAVER_DONOR = "40"
        LIFE_PARTNER = "53"
        OTHER_RELATIONSHIP = "G8"

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
    individual_relationship_code: IndividualRelationshipCode
    claim_filing_indicator_code: ClaimFilingIndicatorCode


class Loop2320AmtSegment(AmtSegment):
    """
    Other Subscriber COB Payer Paid Amount
    """

    class AmountQualifierCode(str, Enum):
        """
        Code values for AMT01
        """

        PAYOR_AMOUNT_PAID = "D"
        AMOUNT_OWED = "EAF"
        NONCOVERED_CHARGES_ACTUAL = "A8"

    amount_qualifier_code: AmountQualifierCode


class Loop2330aNm1Segment(Nm1Segment):
    """
    Claim Other Subscriber Name
    """

    class IdentificationCodeQualifier(str, Enum):
        """
        Code values for NM108
        """

        STANDARD_HEALTH_ID_US = "II"
        MEMBER_IDENTIFICATION_NUMBER = "MI"

    entity_identifier_code: Literal["IL"]
    identification_code_qualifier: IdentificationCodeQualifier
    identification_code: str = Field(min_length=2, max_length=80)


class Loop2330aRefSegment(RefSegment):
    """
    Claim Other Subscriber Reference Identification
    """

    reference_identification_qualifier: Literal["SY"]


class Loop2330bNm1Segment(Nm1Segment):
    """
    Claim Other Subscriber Other Payer Name
    """

    class IdentificationCodeQualifier(str, Enum):
        """
        Code values for NM108
        """

        PAYOR_IDENTIFICATION = "PI"
        CMS_PLAN_ID = "XV"

    entity_identifier_code: Literal["PR"]
    entity_type_qualifier: Literal["2"]
    name_last_or_organization_name: str = Field(min_length=1, max_length=60)
    identification_code_qualifier: IdentificationCodeQualifier
    identification_code: str = Field(min_length=2, max_length=80)


class Loop2330BDtpSegment(DtpSegment):
    """
    Claim Other Subscriber Other Payer Claim Check or Remittance Date
    """

    date_time_qualifier: Literal["573"]
    date_time_period_format_qualifier: Literal["D8"]


class Loop2300BRefSegment(RefSegment):
    """
    Claim Other Subscriber Other Payer Reference Identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        PAYER_IDENTIFICATION_NUMBER = "2U"
        EMPLOYER_IDENTIFICATION_NUMBER = "EI"
        CLAIM_OFFICE_NUMBER = "FY"
        NAIC_CODE = "NF"
        PRIOR_AUTHORIZATION_NUMBER = "G1"
        REFERRAL_NUMBER = "9F"
        SIGNAL_CODE = "T4"
        ORIGINAL_REFERENCE_NUMBER = "F8"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2330cNm1Segment(Nm1Segment):
    """
    Claim Other Subscriber Other Payer Attending Provider Name
    """

    entity_identifier_code: Literal["71"]
    entity_type_qualifier: Literal["1"]
    name_last_or_organization_name: Optional[str]


class Loop2330cRefSegment(RefSegment):
    """
    Claim Other Subscriber Other Payer Attending Provider Reference Identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        STATE_LICENSE_NUMBER = "0B"
        PROVIDER_UPIN_NUMBER = "1G"
        PROVIDER_COMMERCIAL_NUMBER = "G2"
        LOCATION_NUMBER = "LU"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2330dNm1Segment(Nm1Segment):
    """
    Claim Other Subscriber Other Payer Operating Physician
    """

    entity_identifier_code: Literal["72"]
    entity_type_qualifier: Literal["1"]
    name_last_or_organization_name: Optional[str]


class Loop2330dRefSegment(RefSegment):
    """
    Claim Other Subscriber Other Payer Operating Physician Reference Identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        STATE_LICENSE_NUMBER = "0B"
        PROVIDER_UPIN_NUMBER = "1G"
        PROVIDER_COMMERCIAL_NUMBER = "G2"
        LOCATION_NUMBER = "LU"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2330eNm1Segment(Nm1Segment):
    """
    Claim Other Subscriber Other Payer Other Operating Physician
    """

    entity_identifier_code: Literal["ZZ"]
    entity_type_qualifier: Literal["1"]
    name_last_or_organization_name: Optional[str]


class Loop2330eRefSegment(RefSegment):
    """
    Claim Other Subscriber Other Payer Other Operating Physician Reference Identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        STATE_LICENSE_NUMBER = "0B"
        PROVIDER_UPIN_NUMBER = "1G"
        PROVIDER_COMMERCIAL_NUMBER = "G2"
        LOCATION_NUMBER = "LU"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2330fNm1Segment(Nm1Segment):
    """
    Claim Other Subscriber Other Payer Service Facility Location
    """

    entity_identifier_code: Literal["77"]
    entity_type_qualifier: Literal["2"]
    name_last_or_organization_name: Optional[str]


class Loop2330fRefSegment(RefSegment):
    """
    Claim Other Subscriber Other Payer Service Facility Location Reference Identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        STATE_LICENSE_NUMBER = "0B"
        PROVIDER_COMMERCIAL_NUMBER = "G2"
        LOCATION_NUMBER = "LU"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2330gNm1Segment(Nm1Segment):
    """
    Claim Other Subscriber Other Payer Rendering Provider Name
    """

    entity_identifier_code: Literal["82"]
    entity_type_qualifier: Literal["1"]
    name_last_or_organization_name: Optional[str]


class Loop2330gRefSegment(RefSegment):
    """
    Claim Other Subscriber Other Payer Rendering Provider Reference Identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        STATE_LICENSE_NUMBER = "0B"
        PROVIDER_UPIN_NUMBER = "1G"
        PROVIDER_COMMERCIAL_NUMBER = "G2"
        LOCATION_NUMBER = "LU"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2330HNm1Segment(Nm1Segment):
    """
    Claim Other Subscriber Other Payer Referring Provider Name
    """

    entity_identifier_code: Literal["DN"]
    entity_type_qualifier: Literal["1"]
    name_last_or_organization_name: Optional[str]


class Loop2330HRefSegment(RefSegment):
    """
    Claim Other Subscriber Other Payer Referring Provider Reference Identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        STATE_LICENSE_NUMBER = "0B"
        PROVIDER_UPIN_NUMBER = "1G"
        PROVIDER_COMMERCIAL_NUMBER = "G2"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2330INm1Segment(Nm1Segment):
    """
    Claim Other Subscriber Other Payer Billing Provider Name
    """

    entity_identifier_code: Literal["85"]
    entity_type_qualifier: Literal["2"]
    name_last_or_organization_name: Optional[str]


class Loop2330IRefSegment(RefSegment):
    """
    Claim Other Subscriber Other Payer Billing Provider Reference Identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        PROVIDER_COMMERCIAL_NUMBER = "G2"
        LOCATION_NUMBER = "LU"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2400DtpSegment(DtpSegment):
    """
    Date values for Loop 2400 - Claim service line
    """

    date_time_qualifier: Literal["472"]
    date_time_period_format_qualifier: Literal["D8"]


class Loop2400PwkSegment(PwkSegment):
    """
    Service line paperwork segment
    """

    class AttachmentReportTypeCode(str, Enum):
        """
        PWK01 code values
        """

        REPORT_JUSTIFYING_TREATMENT_BEYOND_UTILIZATION_GUIDELINES = "03"
        DRUGS_ADMINISTERED = "04"
        TREATMENT_DIAGNOSIS = "05"
        INITIAL_ASSESSMENT = "06"
        FUNCTIONAL_GOALS = "07"
        PLAN_OF_TREATMENT = "08"
        PROGRESS_REPORT = "09"
        CONTINUED_TREATMENT = "10"
        CHEMICAL_ANALYSIS = "11"
        CERTIFIED_TEST_REPORT = "13"
        JUSTIFICATION_FOR_ADMISSION = "15"
        RECOVERY_PLAN = "21"
        ALLERGIES_SENSITIVITIES_DOCUMENT = "A3"
        AUTOPSY_REPORT = "A4"
        AMBULANCE_CERTIFICATION = "AM"
        ADMISSION_SUMMARY = "AS"
        PRESCRIPTION = "B2"
        PHYSICIAN_ORDER = "B3"
        REFERRAL_FORM = "B4"
        BENCHMARK_TESTING_RESULTS = "BR"
        BASELINE = "BS"
        BLANKET_TESTING_RESULTS = "BT"
        CHIROPRACTIC_JUSTIFICATION = "CB"
        CONSENT_FORM = "CK"
        CERTIFICATION = "CT"
        DRUG_PROFILE_DOCUMENT = "D2"
        DENTAL_MODELS = "DA"
        DURABLE_MEDICAL_EQUIPMENT_PRESCRIPTION = "DB"
        DIAGNOSTIC_REPORT = "DG"
        DISCHARGE_MONITORING_REPORT = "DJ"
        DISCHARGE_SUMMARY = "DS"
        EXPLANATION_OF_BENEFITS = "EB"
        HEALTH_CERTIFICATE = "HC"
        HEALTH_CLINIC_RECORDS = "HR"
        IMMUNIZATION_RECORD = "I5"
        STATE_SCHOOL_IMMUNIZATION_RECORDS = "IR"
        LABORATORY_RESULTS = "LA"
        MEDICAL_RECORD_ATTACHMENT = "M1"
        MODELS = "MT"
        NURSING_NOTES = "NN"
        OPERATIVE_NOTE = "OB"
        OXYGEN_CONTENT_AVERAGING_REPORT = "OC"
        ORDERS_AND_TREATMENTS_DOCUMENT = "OD"
        OBJECTIVE_PHYSICAL_EXAMINATION = "OE"
        OXYGEN_THERAPY_CERTIFICATION = "OX"
        SUPPORT_DATA_FOR_CLAIM = "OZ"
        PATHOLOGY_REPORT = "P4"
        PATIENT_MEDICAL_HISTORY_DOCUMENT = "P5"
        PARENTAL_OR_ENTERAL_CERTIFICATION = "PE"
        PHYSICAL_THERAPY_NOTES = "PN"
        PROSTHETICS_OR_ORTHOTIC_CERTIFICATION = "PO"
        PARAMEDICAL_RESULTS = "PQ"
        PHYSICIANS_REPORT = "PY"
        PHYSICAL_THERAPY_CERTIFICATION = "PZ"
        RADIOLOGY_FILMS = "RB"
        RADIOLOGY_REPORTS = "RR"
        REPORT_OF_TESTS_AND_ANALYSIS_REPORT = "RT"
        RENEWABLE_OXYGEN_CONTENT_AVERAGING_REPORT = "RX"
        SYMPTOMS_DOCUMENT = "SG"
        DEATH_NOTIFICATION = "V5"
        PHOTOGRAPHS = "XP"

    class AttachmentTransmissionCode(str, Enum):
        """
        Code values for PWK02
        """

        AVAILABLE_ON_REQUEST_PROVIDER_SITE = "AA"
        BY_MAIL = "BM"
        ELECTRONICALLY_ONLY = "EL"
        EMAIL = "EM"
        FILE_TRANSFER = "FT"
        BY_FAX = "FX"

    report_type_code: AttachmentReportTypeCode
    report_transmission_code: AttachmentTransmissionCode


class Loop2400RefSegment(RefSegment):
    """
    Loop 2400/Service Line Reference Identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        PROVIDER_CONTROL_NUMBER = "6R"
        REPRICED_LINE_ITEM_REFERENCE_NUMBER = "9B"
        ADJUSTED_REPRICED_LINE_ITEM_REFERENCE_NUMBER = "9D"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2400AmtSegment(AmtSegment):
    """
    Loop 2400/Service Line Amounts
    """

    class AmountQualifierCode(str, Enum):
        """
        Code values for AMT01
        """

        GOODS_SERVICES_TAX = "GT"
        MISCELLANEOUS_TAXES = "N8"

    amount_qualifier_code: AmountQualifierCode


class Loop2400NteSegment(NteSegment):
    """
    Loop 2400/Claim Service Line Notes
    """

    note_reference_code: Literal["TPO"]


class Loop2410RefSegment(RefSegment):
    """
    Loop 2400/Claim Service Line Drug Identification Reference Identifier
    """

    reference_identification_qualifier: Literal["XZ"]


class Loop2420ANm1Segment(Nm1Segment):
    """
    Loop 2420A Operating Physician Name
    """

    entity_identifier_code: Literal["71"]
    entity_type_qualifier: Literal["1"]
    identification_code_qualifier: Literal["XX"]


class Loop2420ARefSegment(RefSegment):
    """
    Loop 2420A Operating Physician Reference Identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        STATE_LICENSE_NUMBER = "0B"
        PROVIDER_UPIN_NUMBER = "1G"
        PROVIDER_COMMERCIAL_NUMBER = "G2"
        LOCATION_NUMBER = "LU"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2420BNm1Segment(Nm1Segment):
    """
    Loop 2420B Other Operating Physician Name
    """

    entity_identifier_code: Literal["ZZ"]
    entity_type_qualifier: Literal["1"]
    identification_code_qualifier: Optional[Literal["XX"]]


class Loop2420BRefSegment(RefSegment):
    """
    Loop 2420B Purchased Service Provider Reference Identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        STATE_LICENSE_NUMBER = "0B"
        PROVIDER_UPIN_NUMBER = "1G"
        PROVIDER_COMMERCIAL_NUMBER = "G2"
        LOCATION_NUMBER = "LU"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2420CNm1Segment(Nm1Segment):
    """
    Loop 2420C Rendering Provider Name
    """

    entity_identifier_code: Literal["82"]
    entity_type_qualifier: Literal["1"]
    identification_code_qualifier: Optional[Literal["XX"]]


class Loop2420CRefSegment(RefSegment):
    """
    Loop 2420C Rendering Provider Reference Identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        STATE_LICENSE_NUMBER = "0B"
        PROVIDER_UPIN_NUMBER = "1G"
        PROVIDER_COMMERCIAL_NUMBER = "G2"
        LOCATION_NUMBER = "LU"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2420DNm1Segment(Nm1Segment):
    """
    Loop 2420D Referring Provider Name
    """

    entity_identifier_code: Literal["DN"]
    entity_type_qualifier: Literal["1"]
    identification_code_qualifier: Optional[Literal["XX"]]


class Loop2420DRefSegment(RefSegment):
    """
    Loop 2420D Referring Provider Reference Identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        STATE_LICENSE_NUMBER = "0B"
        PROVIDER_UPIN_NUMBER = "1G"
        PROVIDER_COMMERCIAL_NUMBER = "G2"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2430DtpSegment(DtpSegment):
    """
    Loop 2430 Line Check or Remittance Date
    """

    date_time_qualifier: Literal["573"]
    date_time_period_format_qualifier: Literal["D8"]


class Loop2430AmtSegment(AmtSegment):
    """
    Loop 2430 Remaining Patient Liability
    """

    amount_qualifier_code: Literal["EAF"]
