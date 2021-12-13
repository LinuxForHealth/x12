"""
segments.py

Specialized segment models for the HealthCare Claim Professional 837 005010X222A2 transaction.
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
    QtySegment,
    PwkSegment,
)
from typing import Literal, Optional, Dict
from enum import Enum
from pydantic import Field, root_validator


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


class Loop2000CHlSegment(HlSegment):
    """
    The HL segment for Loop 2000C (Patient)
    """

    hierarchical_level_code: Literal["23"]


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
    identification_code_qualifier: IdentificationCodeQualifier


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


class Loop2010CaPerSegment(PerSegment):
    """
    Loop2010CA (Patient Name) Per (Contact) segment
    """

    communication_number_qualifier_1: Literal["TE"]
    communication_number_qualifier_2: Optional[Literal["EX"]]


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

        ONSET_OF_CURRENT_SYMPTOM_OR_ILLNESS = "431"
        INITIAL_TREATMENT = "454"
        LAST_VISIT_OR_CONSULTATION = "304"
        ACUTE_MANIFESTATION_OF_CHRONIC_CONDITION = "453"
        ACCIDENT = "439"
        LAST_MENSTRUAL_PERIOD = "484"
        LAST_XRAY = "455"
        PRESCRIPTION = "471"
        DISABILITY = "314"
        INITIAL_DISABILITY_START = "360"
        INITIAL_DISABILITY_END = "361"
        INITIAL_DISABILITY_LAST_DATE_WORKED = "297"
        INITIAL_DISABILITY_RETURN_TO_WORK = "296"
        ADMISSION = "435"
        DISCHARGE = "096"
        ASSUMED_CARE_DATE = "090"
        RELINQUISHED_CARE_DATE = "091"
        FIRST_VISIT_CONSULTATION = "444"
        REPRICER_RECEIVED_DATE = "050"

    class DateTimePeriodFormatQualifier(str, Enum):
        """
        Code values for DTP02
        """

        DATE = "D8"
        DATE_RANGE = "RD8"

    date_time_qualifier: DateTimeQualifier
    date_time_period_format_qualifier: DateTimePeriodFormatQualifier

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

    amount_qualifier_code: Literal["F5"]


class Loop2300RefSegment(RefSegment):
    """
    Claim information reference identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        SPECIAL_PAYMENT_REFERENCE_NUMBER = "4N"
        MEDICARE_VERSION_CODE = "F5"
        MAMMOGRAPHY_CERTIFICATION_NUMBER = "EW"
        REFERRAL_NUMBER = "9F"
        PRIOR_AUTHORIZATION_NUMBER = "G1"
        ORIGINAL_REFERENCE_NUMBER = "F8"
        CLINICAL_LABORATORY_IMPROVEMENT_AMENDMENT_NUMBER = "X4"
        REPRICED_CLAIM_REFERENCE_NUMBER = "9A"
        ADJUSTED_REPRICED_CLAIM_REFERENCE_NUMBER = "9C"
        QUALIFIED_PRODUCTS_LIST = "LX"
        CLAIM_NUMBER = "D9"
        MEDICAL_RECORD_IDENTIFICATION_NUMBER = "EA"
        PROJECT_CODE = "P4"
        FACILITY_ID_NUMBER = "1J"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2300NteSegment(NteSegment):
    """
    Claim information note segment
    """

    class NoteReferenceCode(str, Enum):
        """
        Code values for NTE01
        """

        ADDITIONAL_INFORMATION = "ADD"
        CERTIFICATION_NARRATIVE = "CER"
        GOALS_REHAB_POTENTIAL_DISCHARGE_PLANS = "DCP"
        DIAGNOSIS_DESCRIPTION = "DGN"
        THIRD_PARTY_ORGANIZATION_NOTES = "TPO"

    note_reference_code: NoteReferenceCode


class Loop2300CrcAmbulanceCertification(CrcSegment):
    """
    Claim Information - Ambulance Certification
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

        PATIENT_ADMITTED_TO_HOSPITAL = "01"
        PATIENT_MOVED_BY_STRETCHER = "04"
        PATIENT_UNCONSCIOUS_IN_SHOCK = "05"
        PATIENT_EMERGENCY_TRANSPORT = "06"
        PATIENT_RESTRAINED = "07"
        PATIENT_HEMORRHAGING = "08"
        AMBULANCE_MEDICALLY_NECESSARY = "09"
        PATIENT_CONFINED_BED_CHAIR = "12"

    code_category: Literal["07"]
    certification_condition_indicator: YesNoResponseCode
    condition_code_1: ConditionsIndicator
    condition_code_2: Optional[ConditionsIndicator]
    condition_code_3: Optional[ConditionsIndicator]
    condition_code_4: Optional[ConditionsIndicator]
    condition_code_5: Optional[ConditionsIndicator]


class Loop2300CrcPatientConditionVision(CrcSegment):
    """
    Claim Information - Patient Vision Condition
    """

    class CodeCategoryValues(str, Enum):
        """
        Code values for CRC01
        """

        SPECTACLE_LENSES = "E1"
        CONTACT_LENSES = "E2"
        SPECTACLE_FRAMES = "E3"

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

        GENERAL_STANDARD_20_DEGREE = "L1"
        REPLACEMENT_LOSS_THEFT = "L2"
        REPLACEMENT_BREAKAGE_DAMAGE = "L3"
        REPLACEMENT_PATIENT_PREFERENCE = "L4"
        REPLACEMENT_MEDICAL_REASON = "L5"

    code_category: CodeCategoryValues
    certification_condition_indicator: YesNoResponseCode
    condition_code_1: ConditionsIndicator
    condition_code_2: Optional[ConditionsIndicator]
    condition_code_3: Optional[ConditionsIndicator]
    condition_code_4: Optional[ConditionsIndicator]
    condition_code_5: Optional[ConditionsIndicator]


class Loop2300CrcHomeboundIndicator(CrcSegment):
    """
    Claim Information - Homebound indicator
    """

    class ConditionsIndicator(str, Enum):
        """
        Code values for CRC03 - CRC07
        """

        INDEPENDENT_AT_HOME = "IH"

    code_category: Literal["75"]
    certification_condition_indicator: Literal["Y"]
    condition_code_1: ConditionsIndicator
    condition_code_2: Optional[ConditionsIndicator]
    condition_code_3: Optional[ConditionsIndicator]
    condition_code_4: Optional[ConditionsIndicator]
    condition_code_5: Optional[ConditionsIndicator]


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


class Loop2300CrcSegment(CrcSegment):
    """
    Claim information conditions indicators
    """

    @root_validator
    def validate_specialized_crc_segment(cls, values):
        """
        Parses the CRC segments code category to determine which model is used for validation.
        """
        code_category = values.get("code_category")

        if code_category == "07":
            Loop2300CrcAmbulanceCertification(**values)
        elif code_category in ("E1", "E2", "E3"):
            Loop2300CrcPatientConditionVision(**values)
        elif code_category == "75":
            Loop2300CrcHomeboundIndicator(**values)
        elif code_category == "ZZ":
            Loop2300CrcEpSdtRefferal(**values)
        else:
            raise ValueError(f"Unknown CRC01 code category value {code_category}")
        return values


class Loop2310ANm1Segment(Nm1Segment):
    """
    Claim Referring Provider Name
    """

    class EntityIdentifierCode(str, Enum):
        """
        Code values for NM101
        """

        REFERRING_PROVIDER = "DN"
        PRIMARY_CARE_PROVIDER = "P3"

    entity_identifier_code: EntityIdentifierCode
    entity_type_qualifier: Literal["1"]
    identification_code_qualifier: Optional[Literal["XX"]]


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

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2310BNm1Segment(Nm1Segment):
    """
    Claim Rendering Provider Name
    """

    entity_identifier_code: Literal["82"]
    identification_code_qualifier: Literal["XX"]


class Loop2310BPrvSegment(PrvSegment):
    """
    Claim Rendering Provider Specialty
    """

    provider_code: Literal["PE"]
    reference_identification_qualifier: Literal["PXC"]
    reference_identification: str = Field(min_length=1, max_length=50)


class Loop2310BRefSegment(RefSegment):
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


class Loop2310CaPerSegment(PerSegment):
    """
    Loop2310CA (Patient Name) Per (Contact) segment
    """

    communication_number_qualifier_1: Literal["TE"]
    communication_number_qualifier_2: Optional[Literal["EX"]]


class Loop2310CNm1Segment(Nm1Segment):
    """
    Claim Service Facility Location Name
    """

    entity_identifier_code: Literal["77"]
    entity_type_qualifier: Literal["2"]
    identification_code_qualifier: Optional[Literal["XX"]]
    identification_code: Optional[str]


class Loop2310CRefSegment(RefSegment):
    """
    Claim Service Facility Location Reference Identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        STATE_LICENSE_NUMBER = "0B"
        PROVIDER_COMMERCIAL_NUMBER = "G2"
        LOCATION_NUMBER = "LU"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2310CPerSegment(PerSegment):
    """
    Claim Service Facility Contact Segment
    """

    communication_number_qualifier_1: Literal["TE"]
    communication_number_qualifier_2: Optional[Literal["EX"]]


class Loop2310DNm1Segment(Nm1Segment):
    """
    Claim Supervising Provider Name
    """

    entity_identifier_code: Literal["DQ"]
    entity_type_qualifier: Literal["1"]
    identification_code_qualifier: Literal["XX"]


class Loop2310DRefSegment(Nm1Segment):
    """
    Claim Supervising Provider Reference Identification
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
    Claim ambulance pickup location
    """

    entity_identifier_code: Literal["PW"]
    entity_type_qualifier: Literal["2"]
    name_last_or_organization_name: Optional[str]


class Loop2310FNm1Segment(Nm1Segment):
    """
    Claim ambulance pickup location
    """

    entity_identifier_code: Literal["45"]
    entity_type_qualifier: Literal["2"]
    name_last_or_organization_name: Optional[str]


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

    payer_responsibility_code: PayerResponsibilityCode
    individual_relationship_code: Optional[IndividualRelationshipCode]
    claim_filing_indicator_code: InsuranceTypeCode


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

        PAYOR_IDENTIFICATION = "PI"
        EMPLOYER_IDENTIFICATION_NUMBER = "EI"
        CLAIM_OFFICE_NUMBER = "FY"
        NAIC_CODE = "NF"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2330cNm1Segment(Nm1Segment):
    """
    Claim Other Subscriber Other Payer Referring Provider Name
    """

    class EntityIdentifierCode(str, Enum):
        """
        Code values for NM01
        """

        REFERRING_PROVIDER = "DN"
        PRIMARY_CARE_PROVIDER = "P3"

    entity_identifier_code: EntityIdentifierCode
    entity_type_qualifier: Literal["1"]


class Loop2330cRefSegment(RefSegment):
    """
    Claim Other Subscriber Referring Provider
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        STATE_LICENSE_NUMBER = "0B"
        PROVIDER_UPIN_NUMBER = "1G"
        PROVIDER_COMMERCIAL_NUMBER = "G2"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2330dNm1Segment(Nm1Segment):
    """
    Claim Other Subscriber Other Payer Rendering Provider Name
    """

    entity_identifier_code: Literal["82"]
    name_last_or_organization_name: Optional[str]


class Loop2330dRefSegment(RefSegment):
    """
    Claim Other Subscriber Rendering Provider
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
    Claim Other Subscriber Other Payer Service Facility Location
    """

    entity_identifier_code: Literal["77"]
    entity_type_qualifier: Literal["2"]


class Loop2330eRefSegment(RefSegment):
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


class Loop2330fNm1Segment(Nm1Segment):
    """
    Claim Other Subscriber Other Payer Service Facility Location
    """

    entity_identifier_code: Literal["DQ"]
    entity_type_qualifier: Literal["1"]


class Loop2330fRefSegment(RefSegment):
    """
    Claim Other Subscriber Other Payer Service Facility Location Reference Identification
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


class Loop2330gNm1Segment(Nm1Segment):
    """
    Claim Other Subscriber Other Payer Service Facility Location
    """

    entity_identifier_code: Literal["85"]


class Loop2330gRefSegment(RefSegment):
    """
    Claim Other Subscriber Other Payer Service Facility Location Reference Identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        PROVIDER_COMMERCIAL_NUMBER = "G2"
        LOCATION_NUMBER = "LU"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2400PwkSegment(PwkSegment):
    """
    Service Line information paperwork segment
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


class Loop2400CrcSegment(CrcSegment):
    """
    Conditions Indicator
    """

    class YesNoResponseCode(str, Enum):
        """
        Code values for CRC
        """

        YES = "Y"
        NO = "N"

    class CodeCategory(str, Enum):
        """
        Code values for CRC01
        """

        DURABLE_MEDICAL_EQUIPMENT_CERTIFICATION = "09"
        HOSPICE = "70"

    class ConditionsIndicator(str, Enum):
        """
        Code values for CRC03 - CRC07
        """

        # Ambulance Conditions
        PATIENT_ADMITTED_TO_HOSPITAL = "01"
        PATIENT_MOVED_BY_STRETCHER = "04"
        PATIENT_UNCONSCIOUS_IN_SHOCK = "05"
        PATIENT_EMERGENCY_TRANSPORT = "06"
        PATIENT_RESTRAINED = "07"
        PATIENT_HEMORRHAGING = "08"
        AMBULANCE_MEDICALLY_NECESSARY = "09"
        PATIENT_CONFINED_BED_CHAIR = "12"
        # Hospice Condition
        OPEN = "65"
        # Durable Medical Equipment Condition
        CERTIFICATE_ON_FILE_SUPPLIER = "38"
        REPLACEMENT_ITEM = "ZV"

    code_category: CodeCategory
    certification_condition_indicator: YesNoResponseCode
    condition_code_1: ConditionsIndicator
    condition_code_2: Optional[ConditionsIndicator]
    condition_code_3: Optional[ConditionsIndicator]
    condition_code_4: Optional[ConditionsIndicator]
    condition_code_5: Optional[ConditionsIndicator]


class Loop2400DtpSegment(DtpSegment):
    """
    Date values for Loop 2400 - Claim service line
    """

    class DateTimeQualifier(str, Enum):
        """
        Code values for DTP001
        """

        SERVICE = "472"
        PRESCRIPTION = "471"
        CERTIFICATION_REVISION = "607"
        BEGIN_THERAPY = "463"
        LAST_CERTIFICATION = "461"
        LATEST_VISIT_CONSULTATION = "304"
        MOST_RECENT_HEMOGLOBIN_HEMATOCRIT = "738"
        MOST_RECENT_SERUM_CREATINE = "739"
        SHIPPED = "011"
        LAST_X_RAY = "455"
        INITIAL_TREATMENT = "454"

    date_time_qualifier: DateTimeQualifier


class Loop2400QtySegment(QtySegment):
    """
    Quantity Information for Claim Service Lines
    """

    class QuantityQualifier(str, Enum):
        """
        Code values for QTY01
        """

        UNITS = "FL"
        PATIENTS = "PT"

    quantity_qualifier: QuantityQualifier


class Loop2400Cn1Segment(Cn1Segment):
    """
    Contract Information
    """

    class ContractTypeCode(str, Enum):
        """
        Code values for CN101
        """

        DIAGNOSIS_RELATED_GROUP = "01"
        PER_DIEM = "02"
        VARIABLE_PER_DIEM = "03"
        FLAT = "04"
        CAPITATED = "05"
        PERCENT = "06"
        OTHER = "09"

    contract_code: ContractTypeCode


class Loop2400RefSegment(RefSegment):
    """
    Loop 2400/Service Line Reference Identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        REPRICED_LINE_ITEM_REFERENCE_NUMBER = "9B"
        ADJUSTED_REPRICED_LINE_ITEM_REFERENCE_NUMBER = "9D"
        PRIOR_AUTHORIZATION_NUMBER = "G1"
        PROVIDER_CONTROL_NUMBER = "6R"
        MAMMOGRAPHY_CERTIFICATION_NUMBER = "EW"
        CLINICAL_LABORATORY_IMPROVEMENT_NUMBER = "X4"
        FACILITY_CERTIFICATION_NUMBER = "F4"
        BATCH_NUMBER = "BT"
        REFERRAL_NUMBER = "9F"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2400AmtSegment(AmtSegment):
    """
    Loop 2400/Service Line Amounts
    """

    class AmountQualifierCode(str, Enum):
        """
        Code values for AMT01
        """

        TAX = "T"
        POSTAGE_CLAIMED = "F4"

    amount_qualifier_code: AmountQualifierCode


class Loop2400NteSegment(NteSegment):
    """
    Loop 2400/Claim Service Line Notes
    """

    class NoteReferenceCode(str, Enum):
        """
        NTE01 code values
        """

        ADDITIONAL_INFORMATION = "ADD"
        GOALS_REHAB_DISCHARGE_PLANS = "DCP"
        THIRD_PARTY_ORGANIZATION_NOTES = "TPO"

    note_reference_code: NoteReferenceCode


class Loop2410RefSegment(RefSegment):
    """
    Loop 2400/Claim Service Line Drug Identification Reference Identifier
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        LINK_SEQUENCE_NUMBER = "VY"
        PHARMACY_PRESCRIPTION_NUMBER = "XZ"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2420ANm1Segment(Nm1Segment):
    """
    Loop 2420A Rendering Provider Name
    """

    entity_identifier_code: Literal["82"]
    identification_code_qualifier: Literal["XX"]


class Loop2420APrvSegment(PrvSegment):
    """
    Loop 2420A Rendering Provider Speciality
    """

    provider_code: Literal["PE"]
    reference_identification_qualifier: Literal["PXC"]


class Loop2420ARefSegment(RefSegment):
    """
    Loop 2420A Rendering Provider Reference Identification
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
    Loop 2420B Purchased Service Provider Name
    """

    entity_identifier_code: Literal["QB"]
    identification_code_qualifier: Literal["XX"]


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

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2420CNm1Segment(Nm1Segment):
    """
    Loop 2420C Service Facility Location Name
    """

    entity_identifier_code: Literal["77"]


class Loop2420CRefSegment(RefSegment):
    """
    Loop 2420C Service Facility Location Reference Identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        PROVIDER_COMMERCIAL_NUMBER = "G2"
        LOCATION_NUMBER = "LU"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2420DNm1Segment(Nm1Segment):
    """
    Loop 2420D Supervising Provider Name
    """

    entity_identifier_code: Literal["DQ"]


class Loop2420DRefSegment(RefSegment):
    """
    Loop 2420D Supervising Provider Reference Identification
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


class Loop2420ENm1Segment(Nm1Segment):
    """
    Loop 2420E Ordering Provider Name
    """

    entity_identifier_code: Literal["DK"]
    entity_type_qualifier: Literal["1"]


class Loop2420ERefSegment(RefSegment):
    """
    Loop 2420E Ordering Provider Reference Identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        STATE_LICENSE_NUMBER = "0B"
        PROVIDER_UPIN_NUMBER = "1G"
        PROVIDER_COMMERCIAL_NUMBER = "G2"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2420EPerSegment(PerSegment):
    """
    Loop 2420E Ordering Provider Contact Information
    """

    class CommunicationNumberQualifier(str, Enum):
        """
        Code values for PER03, PER05, PER07
        """

        ELECTRONIC_MAIL = "EM"
        TELEPHONE_EXTENSION = "EX"
        FACSIMILE = "FX"
        TELEPHONE = "TE"

    communication_number_qualifier_1: CommunicationNumberQualifier
    communication_number_qualifier_2: Optional[CommunicationNumberQualifier]
    communication_number_qualifier_3: Optional[CommunicationNumberQualifier]


class Loop2420FNm1Segment(Nm1Segment):
    """
    Loop 2420C Service Facility Location Name
    """

    class EntityIdentifierCode(str, Enum):
        """
        Code values for NM101
        """

        REFERRING_PROVIDER = "DN"
        PRIMARY_CARE_PROVIDER = "P3"

    entity_identifier_code: EntityIdentifierCode
    entity_type_qualifier: Literal["1"]


class Loop2420FRefSegment(RefSegment):
    """
    Loop 2420C Service Facility Location Reference Identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        STATE_LICENSE_NUMBER = "0B"
        PROVIDER_UPIN_NUMBER = "1G"
        PROVIDER_COMMERCIAL_NUMBER = "G2"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2420GNm1Segment(Nm1Segment):
    """
    Loop 2420G Ambulance Pickup Location
    """

    entity_identifier_code: Literal["PW"]
    entity_type_qualifier: Literal["2"]


class Loop2420HNm1Segment(Nm1Segment):
    """
    Loop 2420H Ambulance Drop-Off Location
    """

    entity_identifier_code: Literal["45"]
    entity_type_qualifier: Literal["2"]


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
