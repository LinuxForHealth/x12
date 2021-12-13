"""
segments.py

Specialized segment models for the HealthCare Claim Professional 837 004010X096A1 transaction.
"""

from linuxforhealth.x12.v4010.segments import (
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
    PwkSegment,
    Cr7Segment,
    HsdSegment,
    QtySegment,
)
from typing import Literal, Optional, Dict
from enum import Enum
from pydantic import Field, root_validator


class HeaderStSegment(StSegment):
    """
    Customized ST segment for 837 transaction header
    """

    transaction_set_identifier_code: Literal["837"]
    implementation_convention_reference: Optional[str]


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

        CHARGABLE = "CH"
        REPORTING = "RP"

    hierarchical_structure_code: Literal["0019"]
    transaction_set_purpose_code: PurposeCode
    transaction_type_code: TransactionTypeCode


class HeaderRefSegment(RefSegment):
    """
    Header REF segment/additional identification
    """

    reference_identification_qualifier: Literal["87"]


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
    entity_type_qualifier: Literal["2"]
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

    class ProviderCode(str, Enum):
        """
        Code values for PRV01
        """

        BILLING = "BI"
        PAY_TO = "PT"

    provider_code: ProviderCode
    reference_identification_qualifier: Literal["ZZ"]
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

        PRIMARY = "P"
        SECONDARY = "S"
        TERTIARY = "T"

    class ClaimFilingIndicatorCode(str, Enum):
        """
        SBR09 code values
        """

        SELF_PAY = "09"
        CENTRAL_CERTIFICATION = "10"
        OTHER_NON_FEDERAL_PROGRAMS = "11"
        PREFERRED_PROVIDER_ORGANIZATION = "12"
        POINT_OF_SERVICE = "13"
        EXCLUSIVE_PROVIDER_ORGANIZATION = "14"
        INDEMNITY_INSURANCE = "15"
        HEALTH_MAINTENANCE_ORGANIZATION_MEDICARE_RISK = "16"
        AUTOMOBILE_MEDICAL = "AM"
        BLUE_CROSS_BLUE_SHIELD = "BL"
        CHAMPUS = "CH"
        COMMERICIAL_INSURANCE_COMPANY = "CI"
        DISABILITY = "DS"
        HEALTH_MAINTENANCE_ORGANIZATION = "HM"
        LIABILITY = "LI"
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
    insurance_type_code: Optional[str]


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
        GRANDFATHER_OR_GRANDMOTHER = "04"
        GRANDSON_OR_GRANDDAUGHTER = "05"
        NEPHEW_OR_NIECE = "07"
        FOSTER_CHILD = "10"
        WARD = "15"
        STEPSON_OR_STEPDAUGHTER = "17"
        CHILD = "19"
        EMPLOYEE = "20"
        UNKNOWN = "21"
        HANDICAPPED_DEPENDENT = "22"
        SPONSORED_DEPENDENT = "23"
        DEPENDENT_OF_MINOR_DEPENDENT = "24"
        SIGNIFICANT_OTHER = "29"
        MOTHER = "32"
        FATHER = "33"
        EMANCIPATED_MINOR = "36"
        ORGAN_DONOR = "39"
        CADAVER_DONOR = "40"
        INJURED_PLAINTIFF = "41"
        CHILD_WHERE_INSURED_HAS_NO_FINANCIAL_RESPONSIBILITY = "43"
        LIFE_PARTNER = "53"
        OTHER_RELATIONSHIP = "G8"

    individual_relationship_code: IndividualRelationshipCode


class Loop2010AaNm1Segment(Nm1Segment):
    """
    Billing Provider Name and Identification
    """

    class IdentificationCodeQualifier(str, Enum):
        """
        Code values for NM108
        """

        EMPLOYER_IDENTIFICATION_NUMBER = "24"
        SOCIAL_SECURITY_NUMBER = "34"
        NATIONAL_PROVIDER_IDENTIFIER = "XX"

    entity_identifier_code: Literal["85"]
    identification_code_qualifier: IdentificationCodeQualifier
    identification_code: str = Field(min_length=2, max_length=80)


class Loop2010AaRefSegment(RefSegment):
    """
    Billing Provider Identification Codes
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        STATE_LICENSE_NUMBER = "0B"
        BLUE_CROSS_PROVIDER_NUMBER = "1A"
        BLUE_SHIELD_PROVIDER_NUMBER = "1B"
        MEDICARE_PROVIDER_NUMBER = "1C"
        MEDICAID_PROVIDER_NUMBER = "1D"
        PROVIDER_UPIN_NUMBER = "1G"
        CHAMPUS_IDENTIFICATION_NUMBER = "1H"
        FACILITY_ID_NUMBER = "1J"
        PREFERRED_PROVIDER_ORGANIZATION_NUMBER = "B3"
        HMO_CODE_NUMBER = "BQ"
        EMPLOYER_IDENTIFICATION_NUMBER = "EI"
        CLINIC_NUMBER = "FH"
        PROVIDER_COMMERCIAL_NUMBER = "G2"
        PROVIDER_SITE_NUMBER = "G5"
        LOCATION_NUMBER = "LU"
        SOCIAL_SECURITY_NUMBER = "SY"
        STATE_INDUSTRIAL_ACCIDENT_PROVIDER_NUMBER = "X5"
        # credit card/billing info
        SYSTEM_NUMBER = "06"
        BANK_ASSIGNED_SECURITY_IDENTIFIER = "8U"
        ELECTRONIC_PAYMENT_REFERENCE_NUMBER = "EM"
        STANDARD_INDUSTRY_CLASSIFICATION_CODE = "IJ"
        RATE_CODE_NUMBER = "RB"
        STORE_NUMBER = "ST"
        TERMINAL_CODE = "TT"

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
    Pay to Provider Name and Identification
    """

    class IdentificationCodeQualifier(str, Enum):
        """
        Code values for NM108
        """

        EMPLOYER_IDENTIFICATION_NUMBER = "24"
        SOCIAL_SECURITY_NUMBER = "34"
        NATIONAL_PROVIDER_IDENTIFIER = "XX"

    entity_identifier_code: Literal["87"]
    entity_type_qualifier: Literal["2"]
    identification_code_qualifier: IdentificationCodeQualifier
    identification_code: str = Field(min_length=2, max_length=80)


class Loop2010AbRefSegment(RefSegment):
    """
    Pay to Provider Reference/Secondary Identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        STATE_LICENSE_NUMBER = "0B"
        BLUE_SHIELD_PROVIDER_NUMBER = "1B"
        MEDICARE_PROVIDER_NUMBER = "1C"
        MEDICAID_PROVIDER_NUMBER = "1D"
        PROVIDER_UPIN_NUMBER = "1G"
        CHAMPUS_IDENTIFICATION_NUMBER = "1H"
        FACILITY_ID_NUMBER = "1J"
        PREFERRED_PROVIDER_ORGANIZATION_NUMBER = "B3"
        HMO_CODE_NUMBER = "BQ"
        EMPLOYER_IDENTIFICATION_NUMBER = "EI"
        CLINIC_NUMBER = "FH"
        PROVIDER_COMMERCIAL_NUMBER = "G2"
        PROVIDER_SITE_NUMBER = "G5"
        LOCATION_NUMBER = "LU"
        SOCIAL_SECURITY_NUMBER = "SY"
        STATE_INDUSTRIAL_ACCIDENT_PROVIDER_NUMBER = "X5"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2010BaNm1Segment(Nm1Segment):
    """
    Subscriber Name Segment
    """

    class IdentificationCodeQualifier(str, Enum):
        """
        Code values for NM108
        """

        MEMBER_IDENTIFICATION_NUMBER = "MI"
        MUTUALLY_DEFINED = "ZZ"

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

        MEMBER_IDENTIFICATION_NUMBER = "1W"
        CLIENT_NUMBER = "23"
        INSURANCE_POLICY_NUMBER = "IG"
        SOCIAL_SECURITY_NUMBER = "SY"
        # property and casualty claiom
        AGENCY_CLAIM_NUMBER = "Y4"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2010BcNm1Segment(Nm1Segment):
    """
    Subscriber - Payer Name
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


class Loop2010BcRefSegment(RefSegment):
    """
    Payer Name Reference Identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        PAYER_IDENTIFICATION_NUMBER = "2U"
        CLAIM_OFFICER_NUMBER = "FY"
        NAIC_CODE = "NF"
        FEDERAL_TAXPAYER_IDENTIFICATION_NUMBER = "TJ"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2010BdNm1Segment(Nm1Segment):
    """
    Responsible Party Name
    """

    entity_identifier_code: Literal["QD"]


class Loop2010BbNm1Segment(Nm1Segment):
    """
    Credit/Debit Card Holder Name
    """

    entity_identifier_code: Literal["AO"]
    identification_code_qualifier: Literal["MI"]
    identification_code: str = Field(min_length=2, max_length=80)


class Loop2010BbRefSegment(RefSegment):
    """
    Credit/Debit Card Holder Information
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        ACCEPTABLE_SOURCE_PURCHASER_ID = "AB"
        AUTHORIZATION_NUMBER = "BB"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2010CaNm1Segment(Nm1Segment):
    """
    Loop2010CA NM1 segment for Patient
    """

    class IdentificationCodeQualifier(str, Enum):
        """
        Code values for NM108
        """

        MEMBER_IDENTIFICATION_NUMBER = "MI"
        MUTUALLY_DEFINED = "ZZ"

    entity_identifier_code: Literal["QC"]
    entity_type_qualifier: Literal["1"]
    identification_code_qualifier: Optional[IdentificationCodeQualifier]
    identification_code: Optional[str]


class Loop2010CaRefSegment(RefSegment):
    """
    Loop 2010CA (Patient Name) REF Segment
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        MEMBER_IDENTIFICATION_NUMBER = "1W"
        CLIENT_NUMBER = "23"
        INSURANCE_POLICY_NUMBER = "IG"
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
        STATEMENT_DATE = "434"
        ADMISSION = "435"

    class DateTimePeriodFormatQualifier(str, Enum):
        """
        Code values for DTP02
        """

        TIME = "TM"
        DATE = "D8"
        DATE_TIME = "DT"
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

        ADMISSION_SUMMARY = "AS"
        PRESCRIPTION = "B2"
        PHYSICIAN_ORDER = "B3"
        REFERRAL_FORM = "B4"
        CERTIFICATION = "CT"
        DENTAL_MODELS = "DA"
        DIAGNOSTIC_REPORT = "DG"
        DISCHARGE_SUMMARY = "DS"
        EXPLANATION_OF_BENEFITS = "EB"
        MODELS = "MT"
        NURSING_NOTES = "NN"
        OPERATIVE_NOTE = "OB"
        SUPPORT_DATA_FOR_CLAIM = "OZ"
        PHYSICAL_THERAPY_NOTES = "PN"
        PROSTHETICS_OR_ORTHOTIC_CERTIFICATION = "PO"
        PHYSICAL_THERAPY_CERTIFICATION = "PZ"
        RADIOLOGY_FILMS = "RB"
        RADIOLOGY_REPORTS = "RR"
        REPORT_OF_TESTS_AND_ANALYSIS_REPORT = "RT"

    class AttachmentTransmissionCode(str, Enum):
        """
        Code values for PWK02
        """

        AVAILABLE_ON_REQUEST_PROVIDER_SITE = "AA"
        BY_MAIL = "BM"
        ELECTRONICALLY_ONLY = "EL"
        EMAIL = "EM"
        BY_FAX = "FX"

    report_type_code: AttachmentReportTypeCode
    report_transmission_code: AttachmentTransmissionCode
    identification_code_qualifier: Optional[Literal["AC"]]


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

    class AmountQualifierCode(str, Enum):
        """
        Code values for AMT01
        """

        CLAIM_AMOUNT_DUE = "C5"
        PATIENT_RESPONSIBILITY_ESTIMATED = "F3"
        PATIENT_AMOUNT_PAID = "F5"
        ADJUSTED_REPRICED_CLAIM_REFERENCE_NUMBER = "9C"
        REPRICED_CLAIM_REFERENCE_NUMBER = "9A"

    amount_qualifier_code: AmountQualifierCode


class Loop2300RefSegment(RefSegment):
    """
    Claim information reference identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        ADJUSTED_REPRICED_CLAIM_REFERENCE_NUMBER = "9C"
        REPRICED_CLAIM_REFERENCE_NUMBER = "9A"
        CLAIM_NUMBER = "D9"
        DOCUMENT_IDENTIFICATION_CODE = "DD"
        ORIGINAL_REFERENCE_NUMBER = "F8"
        QUALIFIED_PRODUCTS_LIST = "LX"
        SPECIAL_PAYMENT_REFERENCE_NUMBER = "4N"
        PEER_REVIEW_ORGANIZATION_APPROVAL_NUMBER = "G4"
        REFERRAL_NUMBER = "9F"
        PRIOR_AUTHORIZATION_NUMBER = "G1"
        MEDICAL_RECORD_IDENTIFICATION_NUMBER = "EA"
        PROJECT_CODE = "P4"

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
        GOALS_REHAB_DISCHARGE_PLANS = "DCP"
        DIAGNOSIS_DESCRIPTION = "DGN"
        DME_AND_SUPPLIES = "DME"
        MEDICATIONS = "MED"
        NUTRITIONAL_REQUIREMENTS = "NTR"
        ORDERS_DISCIPLINES_TREATMENTS = "ODT"
        FUNCTIONAL_LIMITATIONS_HOMEBOUND = "RHB"
        REASONS_PATIENT_LEAVES_HOME = "RLH"
        TIMES_REASON_PATIENT_NOT_AT_HOME = "RNH"
        UNUSUAL_HOME_SOCIAL_ENVIRONMENT = "SET"
        SAFETY_MEASURES = "SFM"
        SUPPLEMENTARY_PLAN_OF_TREATMENT = "SPT"
        UPDATED_INFORMATION = "UPI"
        ADDITIONAL_INFORMATION = "ADD"

    note_reference_code: NoteReferenceCode


class Loop2300CrcHomeboundIndicator(CrcSegment):
    """
    Claim Information - Homebound indicator
    """

    class ConditionsIndicator(str, Enum):
        """
        Code values for CRC03 - CRC07
        """

        AMPUTATION = "AA"
        AMBULATION_LIMITATIONS = "AL"
        BOWEL_BLADDER_LIMITATIONS = "BL"
        CONTRACTURE = "CO"
        DYSPNEA_MINIMAL_EXERTION = "DY"
        ENDURANCE_LIMITATIONS = "EL"
        HEARING_LIMITATIONS = "HL"
        LEGALLY_BLIND = "LB"
        OTHER_LIMITATIONS = "OL"
        PARALYSIS = "PA"
        SPEECH_LIMITATIONS = "SL"

    class CertificationConditionIndicator(str, Enum):
        """
        Code values for CRC02
        """

        NO = "N"
        YES = "Y"

    code_category: Literal["75"]
    certification_condition_indicator: CertificationConditionIndicator
    condition_code_1: ConditionsIndicator
    condition_code_2: Optional[ConditionsIndicator]
    condition_code_3: Optional[ConditionsIndicator]
    condition_code_4: Optional[ConditionsIndicator]
    condition_code_5: Optional[ConditionsIndicator]


class Loop2300CrcHomeHealthActivitiesPermitted(CrcSegment):
    """
    Claim Information - Homebound indicator
    """

    class ConditionsIndicator(str, Enum):
        """
        Code values for CRC03 - CRC07
        """

        BEDREST_BATHROOOM_PRIVILEGES = "BR"
        CANE_REQUIRED = "CA"
        COMPLETE_BEDREST = "CB"
        CRUTCHES_REQUIRED = "CR"
        EXERCISES_PRESCRIBED = "EP"
        INDEPENDENT_AT_HOME = "IH"
        NO_RESTRICTIONS = "NR"
        PARTIAL_WEIGHT_BEARING = "PW"
        TRANSFER_TO_BED_CHAIR = "TR"
        UP_AS_TOLERATED = "UT"
        WALKER_REQUIRED = "WA"
        WHEELCHAIR_REQUIRED = "WR"

    class CertificationConditionIndicator(str, Enum):
        """
        Code values for CRC02
        """

        NO = "N"
        YES = "Y"

    code_category: Literal["76"]
    certification_condition_indicator: CertificationConditionIndicator
    condition_code_1: ConditionsIndicator
    condition_code_2: Optional[ConditionsIndicator]
    condition_code_3: Optional[ConditionsIndicator]
    condition_code_4: Optional[ConditionsIndicator]
    condition_code_5: Optional[ConditionsIndicator]


class Loop2300CrcHomeHealthMentalStatus(CrcSegment):
    """
    Claim Information - Homebound indicator
    """

    class ConditionsIndicator(str, Enum):
        """
        Code values for CRC03 - CRC07
        """

        AGITATED = "AG"
        COMATOSE = "CM"
        DISORIENTED = "DI"
        DEPRESSED = "DP"
        FORGETFUL = "FO"
        LETHARGIC = "LE"
        OTHER_MENTAL_CONDITION = "MC"
        ORIENTED = "OT"

    class CertificationConditionIndicator(str, Enum):
        """
        Code values for CRC02
        """

        NO = "N"
        YES = "Y"

    code_category: Literal["77"]
    certification_condition_indicator: CertificationConditionIndicator
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

        if code_category == "75":
            Loop2300CrcHomeboundIndicator(**values)
        elif code_category == "76":
            Loop2300CrcHomeHealthActivitiesPermitted(**values)
        elif code_category == "77":
            Loop2300CrcHomeHealthMentalStatus(**values)
        else:
            raise ValueError(f"Unknown CRC01 code category value {code_category}")
        return values


class Loop2300QtySegment(QtySegment):
    """
    Claim Quantity
    """

    class QuantityQualifier(str, Enum):
        """
        Code values for QTY01
        """

        COVERED_ACTUAL = "CA"
        COINSURED_ACTUAL = "CD"
        LIFE_TERM_RESERVE_ACTUAL = "LA"
        NUMBER_NON_COVERED_DAYS = "NA"

    quantity_qualifier: QuantityQualifier


class Loop2305Cr7Segment(Cr7Segment):
    """
    Home Health Care Plan Treatment Plan Certification
    """

    class DisciplineTypeCode(str, Enum):
        """
        Code values for CR701
        """

        HOME_HEALTH_AIDE = "AI"
        MEDICAL_SOCIAL_WORKER = "MS"
        OCCUPATIONAL_THERAPY = "OT"
        PHYSICAL_THERAPY = "PT"
        SKILLED_NURSING = "SN"
        SPEECH_THERAPY = "ST"

    discipline_type_code: DisciplineTypeCode


class Loop2305HsdSegment(HsdSegment):
    """
    Home Health Care Plan Treatment Plan Information
    """

    class MeasurementCode(str, Enum):
        """
        HSD03 code values
        """

        DAYS = "DA"
        MONTHS = "MO"
        QUARTER = "Q1"
        WEEK = "WK"

    class TimePeriodQualifier(str, Enum):
        """
        HD05 code values
        """

        DAY = "7"
        WEEK = "35"

    class DeliveryFrequencyCode(str, Enum):
        """
        HSD07 code values
        """

        FIRST_WEEK_OF_MONTH = "1"
        SECOND_WEEK_OF_MONTH = "2"
        THIRD_WEEK_OF_MONTH = "3"
        FOURTH_WEEK_OF_MONTH = "4"
        FIFTH_WEEK_OF_MONTH = "5"
        FIRST_AND_THIRD_WEEKS_OF_MONTH = "6"
        SECOND_AND_FOURTH_WEEKS_OF_MONTH = "7"
        FIRST_WORKING_DAY_OF_PERIOD = "8"
        LAST_WORKING_DAY_OF_PERIOD = "9"
        MONDAY_TO_FRIDAY = "A"
        MONDAY_TO_SATURDAY = "B"
        MONDAY_TO_SUNDAY = "C"
        MONDAY = "D"
        TUESDAY = "E"
        WEDNESDAY = "F"
        THURSDAY = "G"
        FRIDAY = "H"
        SATURDAY = "J"
        SUNDAY = "K"
        MONDAY_TO_THURSDAY = "L"
        AS_DIRECTED = "N"
        DAILY_MON_TO_FRI = "O"
        ONCE_ANYTIME_MON_TO_FRI = "S"
        SUN_MON_THURS_FRI_SAT = "SA"
        TUES_THROUGH_SAT = "SB"
        SUN_WED_THURS_FRI_SAT = "SC"
        MON_WED_THURS_FRI_SAT = "SD"
        TUESDAY_TO_FRIDAY = "SG"
        MONDAY_TUESDAY_THURSDAY = "SL"
        MONDAY_TUESDAY_FRIDAY = "SP"
        WEDNESDAY_THURSDAY = "SX"
        MONDAY_WEDNESDAY_THURSDAY = "SY"
        TUESDAY_THURSDAY_FRIDAY = "SZ"
        WHENEVER_NECESSARY = "W"

    class DeliveryPatternTimeCode(str, Enum):
        """
        HSD08 code values
        """

        AM = "D"
        PM = "E"
        AS_DIRECTED = "F"

    quantity_qualifier: Literal["VS"]
    measurement_code: Optional[MeasurementCode]
    time_period_qualifier: Optional[TimePeriodQualifier]
    delivery_frequency_code: Optional[DeliveryFrequencyCode]
    delivery_pattern_time_code: Optional[DeliveryPatternTimeCode]


class Loop2310ANm1Segment(Nm1Segment):
    """
    Claim Attending Physician Name
    """

    class IdentificationCodeQualifier(str, Enum):
        """
        Code values for NM108
        """

        EMPLOYER_IDENTIFICATION_NUMBER = "24"
        SOCIAL_SECURITY_NUMBER = "34"
        NATIONAL_PROVIDER_IDENTIFIER = "XX"

    entity_identifier_code: Literal["71"]
    identification_code_qualifier: IdentificationCodeQualifier
    identification_code: str = Field(min_length=2, max_length=80)


class Loop2310APrvSegment(PrvSegment):
    """
    Attending Physician Speciality Information
    """

    class ProviderCode(str, Enum):
        """
        Code values for PRV01
        """

        ATTENDING = "AT"
        SUPERVISING = "SU"

    provider_code: ProviderCode
    reference_identification_qualifier: Literal["ZZ"]
    reference_identification: str = Field(min_length=1, max_length=30)


class Loop2310ARefSegment(RefSegment):
    """
    Claim Attending Physician Reference Identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        STATE_LICENSE_NUMBER = "0B"
        BLUE_CROSS_PROVIDER_NUMBER = "1A"
        BLUE_SHIELD_PROVIDER_NUMBER = "1B"
        MEDICARE_PROVIDER_NUMBER = "1C"
        MEDICAID_PROVIDER_NUMBER = "1D"
        PROVIDER_UPIN_NUMBER = "1G"
        CHAMPUS_IDENTIFICATION = "1H"
        EMPLOYERS_IDENTIFICATION_NUMBER = "EI"
        PROVIDER_COMMERCIAL_NUMBER = "G2"
        LOCATION_NUMBER = "LU"
        PROVIDER_PLAN_NETWORK_IDENTIFICATION_NUMBER = "N5"
        SOCIAL_SECURITY_NUMBER = "SY"
        STATE_INDUSTRIAL_ACCIDENT_PROVIDER_NUMBER = "X5"

    reference_identification_qualifier: ReferenceIdentificationQualifier
    reference_identification: str = Field(min_length=1, max_length=30)


class Loop2310BNm1Segment(Nm1Segment):
    """
    Claim Operating Physician
    """

    class IdentificationCodeQualifier(str, Enum):
        """
        Code values for NM108
        """

        EMPLOYER_IDENTIFICATION_NUMBER = "24"
        SOCIAL_SECURITY_NUMBER = "34"
        NATIONAL_PROVIDER_IDENTIFIER = "XX"

    entity_identifier_code: Literal["72"]
    entity_type_qualifier: Literal["1"]
    identification_code_qualifier: IdentificationCodeQualifier
    identification_code: str = Field(min_length=2, max_length=80)


class Loop2310BPrvSegment(PrvSegment):
    """
    Claim Rendering Provider Specialty
    """

    provider_code: Literal["PE"]
    reference_identification_qualifier: Literal["ZZ"]
    reference_identification: str = Field(min_length=1, max_length=30)


class Loop2310BRefSegment(RefSegment):
    """
    Claim Rendering Provider Reference Identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        STATE_LICENSE_NUMBER = "0B"
        BLUE_CROSS_PROVIDER_NUMBER = "1A"
        BLUE_SHIELD_PROVIDER_NUMBER = "1B"
        MEDICARE_PROVIDER_NUMBER = "1C"
        MEDICAID_PROVIDER_NUMBER = "1D"
        PROVIDER_UPIN_NUMBER = "1G"
        CHAMPUS_IDENTIFICATION = "1H"
        EMPLOYERS_IDENTIFICATION_NUMBER = "EI"
        PROVIDER_COMMERCIAL_NUMBER = "G2"
        LOCATION_NUMBER = "LU"
        PROVIDER_PLAN_NETWORK_IDENTIFICATION = "NS"
        SOCIAL_SECURITY_NUMBER = "SY"
        STATE_INDUSTRIAL_ACCOUNT_PROVIDER_NUMBER = "X5"

    reference_identification_qualifier: ReferenceIdentificationQualifier
    reference_identification: str = Field(min_length=1, max_length=30)


class Loop2310CNm1Segment(Nm1Segment):
    """
    Other Provider Name
    """

    class IdentificationCodeQualifier(str, Enum):
        """
        Code values for NM108
        """

        EMPLOYER_IDENTIFICATION_NUMBER = "24"
        SOCIAL_SECURITY_NUMBER = "34"
        NATIONAL_PROVIDER_IDENTIFIER = "XX"

    entity_identifier_code: Literal["73"]
    identification_code_qualifier: Optional[IdentificationCodeQualifier]
    identification_code: str = Field(min_length=1, max_length=30)


class Loop2310CRefSegment(RefSegment):
    """
    Other Provider Reference Identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        STATE_LICENSE_NUMBER = "0B"
        BLUE_CROSS_PROVIDER_NUMBER = "1A"
        BLUE_SHIELD_PROVIDER_NUMBER = "1B"
        MEDICARE_PROVIDER_NUMBER = "1C"
        MEDICAID_PROVIDER_NUMBER = "1D"
        PROVIDER_UPIN_NUMBER = "1G"
        CHAMPUS_IDENTIFICATION = "1H"
        EMPLOYERS_IDENTIFICATION_NUMBER = "EI"
        PROVIDER_COMMERCIAL_NUMBER = "G2"
        LOCATION_NUMBER = "LU"
        PROVIDER_PLAN_NETWORK_IDENTIFICATION = "NS"
        SOCIAL_SECURITY_NUMBER = "SY"
        STATE_INDUSTRIAL_ACCOUNT_PROVIDER_NUMBER = "X5"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2310ENm1Segment(Nm1Segment):
    """
    Service Facility Location Name
    """

    class EntityIdentifierCode(str, Enum):
        """
        Code values for NM101
        """

        SERVICE_LOCATION = "77"
        FACILITY = "FA"
        INDEPENDENT_LAB = "LI"
        TESTING_LABORATORY = "TL"

    class IdentificationCodeQualifier(str, Enum):
        """
        Code values for NM108
        """

        EMPLOYER_IDENTIFICATION_NUMBER = "24"
        SOCIAL_SECURITY_NUMBER = "34"
        NATIONAL_PROVIDER_IDENTIFIER = "XX"

    entity_identifier_code: EntityIdentifierCode
    entity_type_qualifier: Literal["2"]
    identification_code_qualifier: Optional[IdentificationCodeQualifier]


class Loop2310ERefSegment(Nm1Segment):
    """
    Service Facility Location Reference Identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        STATE_LICENSE_NUMBER = "0B"
        BLUE_CROSS_PROVIDER_NUMBER = "1A"
        BLUE_SHIELD_PROVIDER_NUMBER = "1B"
        MEDICARE_PROVIDER_NUMBER = "1C"
        MEDICAID_PROVIDER_NUMBER = "1D"
        PROVIDER_UPIN_NUMBER = "1G"
        CHAMPUS_IDENTIFICATION = "1H"
        PROVIDER_COMMERCIAL_NUMBER = "G2"
        LOCATION_NUMBER = "LU"
        PROVIDER_PLAN_NETWORK_IDENTIFICATION = "NS"
        FEDERAL_TAXPAYER_IDENTIFICATION_NUMBER = "TJ"
        CLINICAL_LABORATORY_IMPROVEMENT_AMENDMENT_NUMBER = "X4"
        STATE_INDUSTRIAL_ACCOUNT_PROVIDER_NUMBER = "X5"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2320SbrSegment(SbrSegment):
    """
    Claim Other Subscriber
    """

    class PayerResponsibilityCode(str, Enum):
        """
        Code values for SBR01
        """

        PRIMARY = "P"
        SECONDARY = "S"
        TERTIARY = "T"

    class IndividualRelationshipCode(str, Enum):
        """
        Code values for SBR02
        """

        SPOUSE = "01"
        GRANDFATHER_GRANDMOTHER = "04"
        GRANDSON_GRANDDAUGHTER = "05"
        NEPHEW_NIECE = "07"
        FOSTER_CHILD = "10"
        WARD = "15"
        STEPSON_STEPDAUGHTER = "17"
        SELF = "18"
        CHILD = "19"
        EMPLOYEE = "20"
        UNKNOWN = "21"
        HANDICAPPED_DEPENDENT = "22"
        SPONSORED_DEPENDENT = "23"
        DEPENDENT_OF_MINOR_DEPENDENT = "24"
        SIGNIFICANT_OTHER = "29"
        MOTHER = "32"
        FATHER = "33"
        EMANCIPATED_MINOR = "36"
        ORGAN_DONOR = "39"
        CADAVER_DONOR = "40"
        INJURED_PLAINTIFF = "41"
        CHILD_WHERE_INSURED_HAS_NO_FINANCIAL_RESPONSIBILITY = "43"
        LIFE_PARTNER = "53"
        OTHER_RELATIONSHIP = "G8"

    class ClaimFilingIndicatorCode(str, Enum):
        """
        Code values for SBR09
        """

        SELF_PAY = "09"
        CENTRAL_CERTIFICATION = "10"
        OTHER_NON_FEDERAL_PROGRAMS = "11"
        PREFERRED_PROVIDER_ORGANIZATION = "12"
        POINT_OF_SERVICE = "13"
        EXCLUSIVE_PROVIDER_ORGANIZATION = "14"
        INDEMNITY_INSURANCE = "15"
        HMO_MEDICARE_RISK = "16"
        AUTOMOBILE_MEDICAL = "AM"
        BLUE_CROSS_BLUE_SHIELD = "BL"
        CHAMPUS = "CH"
        COMMERCIAL_INSURANCE_CO = "CI"
        DISABILITY = "DS"
        HMO = "HM"
        LIABILITY = "LI"
        LIABILITY_MEDICAL = "LM"
        MEDICARE_PART_A = "MA"
        MEDICARE_PART_B = "MB"
        MEDICAID = "MC"
        OTHER_FEDERAL_PROGRAM = "OF"
        TITLE_V = "TV"
        VETERANS_ADMIN_PLAN = "VA"
        WORKERS_COMPENSATION_HEALTH_CLAIM = "WC"
        MUTUALLY_DEFINED_UNKNOWN = "ZZ"

    payer_responsibility_code: PayerResponsibilityCode
    individual_relationship_code: IndividualRelationshipCode
    insurance_type_code: Optional[str]
    claim_filing_indicator_code: ClaimFilingIndicatorCode


class Loop2320AmtSegment(AmtSegment):
    """
    Claim Other Subscriber Amounts
    """

    class AmountQualifierCode(str, Enum):
        """
        Code values for AMT01
        """

        PRIOR_PAYMENT_AMOUNT_ACTUAL = "C4"
        ALLOWED_ACTUAL = "B6"
        TOTAL_SUBMITTED_CHARGES = "T3"
        NET_WORTH = "N1"
        NET_PAID_AMOUNT = "KF"
        PAYOFF = "PG"
        ALLOCATED = "AA"
        BENEFIT_AMOUNT = "B1"
        NON_COVERED_CHARGES_ACTUAL = "A"
        DENIED = "YT"

    amount_qualifier_code: AmountQualifierCode


class Loop2330aNm1Segment(Nm1Segment):
    """
    Claim Other Subscriber Name
    """

    class IdentificationCodeQualifier(str, Enum):
        """
        Code values for NM108
        """

        MEMBER_IDENTIFICATION_NUMBER = "MI"
        MUTUALLY_DEFINED = "ZZ"

    entity_identifier_code: Literal["IL"]
    identification_code_qualifier: IdentificationCodeQualifier
    identification_code: str = Field(min_length=2, max_length=80)


class Loop2330aRefSegment(RefSegment):
    """
    Claim Other Subscriber Reference Identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        MEMBER_IDENTIFICATION_NUMBER = "1W"
        CLIENT_NUMBER = "23"
        INSURANCE_POLICY_NUMBER = "IG"
        SOCIAL_SECURITY_NUMBER = "SY"

    reference_identification_qualifier: ReferenceIdentificationQualifier


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


class Loop2330BRefSegment(RefSegment):
    """
    Claim Other Subscriber Other Payer Reference Identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        PAYER_IDENTIFICATION_NUMBER = "2U"
        ORIGINAL_REFERENCE_NUMBER = "F8"
        CLAIM_OFFICE_NUMBER = "FY"
        NAIC_CODE = "NF"
        FEDERAL_TAXPAYER_IDENTIFICATION_NUMBER = "TJ"
        REFERRAL_NUMBER = "9F"
        PRIOR_AUTHORIZATION_NUMBER = "G1"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2300BRefSegment(RefSegment):
    """
    Claim Other Subscriber Other Payer Reference Identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        PAYER_IDENTIFICATION_NUMBER = "2U"
        ORIGINAL_REFERENCE_NUMBER = "F8"
        CLAIM_OFFICE_NUMBER = "FY"
        NAIC_CODE = "NF"
        FEDERAL_TAXPAYER_IDENTIFIER = "TJ"
        REFERRAL_NUMBER = "9F"
        PRIOR_AUTHORIZATION_NUMBER = "G1"
        SIGNAL_CODE = "T4"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2330cNm1Segment(Nm1Segment):
    """
    Claim Other Subscriber Other Payer Patient Information
    """

    class IdentificationCodeQualifier(str, Enum):
        """
        Code values for NM108
        """

        EMPLOYEE_IDENTIFICATION_NUMBER = "EI"
        MEMBER_IDENTIFICATION_NUMBER = "MI"

    entity_identifier_code: Literal["QC"]
    entity_type_qualifier: Literal["1"]
    identification_code_qualifier: IdentificationCodeQualifier
    identification_code: str = Field(min_length=2, max_length=80)


class Loop2330cRefSegment(RefSegment):
    """
    Claim Other Subscriber Other Payer Patient Identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        MEMBER_IDENTIFICATION_NUMBER = "1W"
        INSURANCE_POLICY_NUMBER = "IG"
        SOCIAL_SECURITY_NUMBER = "SY"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2330dNm1Segment(Nm1Segment):
    """
    Claim Other Subscriber Other Payer Attending Provider
    """

    entity_identifier_code: Literal["71"]
    name_last_or_organization_name: Optional[str]
    identification_code_qualifier: Optional[str]
    identification_code: Optional[str]


class Loop2330dRefSegment(RefSegment):
    """
    Claim Other Subscriber Other Payer Attending Provider
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        BLUE_CROSS_PROVIDER_NUMBER = "1A"
        BLUE_SHIELD_PROVIDER_NUMBER = "1B"
        MEDICARE_PROVIDER_NUMBER = "1C"
        MEDICAID_PROVIDER_NUMBER = "1D"
        PROVIDER_UPIN_NUMBER = "1G"
        CHAMPUS_IDENTIFICATION_NUMBER = "1H"
        EMPLOYERS_IDENTIFICATION_NUMBER = "EI"
        PROVIDER_COMMERCIAL_NUMBER = "G2"
        LOCATION_NUMBER = "LU"
        PROVIDER_PLAN_NETWORK_IDENTIFICATION = "N5"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2330eNm1Segment(Nm1Segment):
    """
    Claim Other Subscriber Other Payer Operating Provider
    """

    entity_identifier_code: Literal["72"]
    entity_type_qualifier: Literal["1"]
    name_last_or_organization_name: Optional[str]


class Loop2330eRefSegment(RefSegment):
    """
    Claim Other Subscriber Other Payer Operating Provider
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        BLUE_CROSS_PROVIDER_NUMBER = "1A"
        BLUE_SHIELD_PROVIDER_NUMBER = "1B"
        MEDICARE_PROVIDER_NUMBER = "1C"
        MEDICAID_PROVIDER_NUMBER = "1D"
        PROVIDER_UPIN_NUMBER = "1G"
        CHAMPUS_IDENTIFICATION_NUMBER = "1H"
        EMPLOYERS_IDENTIFICATION_NUMBER = "EI"
        PROVIDER_COMMERCIAL_NUMBER = "G2"
        LOCATION_NUMBER = "LU"
        PROVIDER_PLAN_NETWORK_IDENTIFICATION = "N5"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2330fNm1Segment(Nm1Segment):
    """
    Claim Other Subscriber Other Payer Other Provider
    """

    entity_identifier_code: Literal["73"]
    name_last_or_organization_name: Optional[str]


class Loop2330fRefSegment(RefSegment):
    """
    Claim Other Subscriber Other Payer Purchased Service Provider Identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        BLUE_CROSS_PROVIDER_NUMBER = "1A"
        BLUE_SHIELD_PROVIDER_NUMBER = "1B"
        MEDICARE_PROVIDER_NUMBER = "1C"
        MEDICAID_PROVIDER_NUMBER = "1D"
        PROVIDER_UPIN_NUMBER = "1G"
        CHAMPUS_IDENTIFICATION_NUMBER = "1H"
        EMPLOYERS_IDENTIFICATION_NUMBER = "EI"
        PROVIDER_COMMERCIAL_NUMBER = "G2"
        LOCATION_NUMBER = "LU"
        PROVIDER_PLAN_NETWORK_IDENTIFICATION = "N5"
        SOCIAL_SECURITY_NUMBER = "SY"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2330HNm1Segment(Nm1Segment):
    """
    Claim Other Subscriber Other Payer Supervising Provider
    """

    entity_identifier_code: Literal["FA"]
    entity_type_qualifier: Literal["2"]
    name_last_or_organization_name: Optional[str]


class Loop2330HRefSegment(RefSegment):
    """
    Claim Other Subscriber Other Payer Supervising Provider Identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        BLUE_SHIELD_PROVIDER_NUMBER = "1B"
        MEDICARE_PROVIDER_NUMBER = "1C"
        MEDICAID_PROVIDER_NUMBER = "1D"
        EMPLOYERS_IDENTIFICATION_NUMBER = "EI"
        PROVIDER_COMMERCIAL_NUMBER = "G2"
        LOCATION_NUMBER = "LU"
        PROVIDER_PLAN_NETWORK_IDENTIFICATION = "N5"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2400PwkSegment(PwkSegment):
    """
    Service Line information paperwork segment
    """

    class AttachmentReportTypeCode(str, Enum):
        """
        PWK01 code values
        """

        ADMISSION_SUMMARY = "AS"
        PRESCRIPTION = "B2"
        PHYSICIAN_ORDER = "B3"
        REFERRAL_FORM = "B4"
        CERTIFICATION = "CT"
        DENTAL_MODELS = "DA"
        DIAGNOSTIC_REPORT = "DG"
        DISCHARGE_SUMMARY = "DS"
        EXPLANATION_OF_BENEFITS = "EB"
        MODELS = "MT"
        NURSING_NOTES = "NN"
        OPERATIVE_NOTE = "OB"
        SUPPORT_DATA_FOR_CLAIM = "OZ"
        PHYSICAL_THERAPY_NOTES = "PN"
        PROSTHETICS_OR_ORTHOTIC_CERTIFICATION = "PO"
        PHYSICAL_THERAPY_CERTIFICATION = "PZ"
        RADIOLOGY_FILMS = "RB"
        RADIOLOGY_REPORTS = "RR"
        REPORT_OF_TESTS_AND_ANALYSIS_REPORT = "RT"

    class AttachmentTransmissionCode(str, Enum):
        """
        Code values for PWK02
        """

        AVAILABLE_ON_REQUEST_PROVIDER_SITE = "AA"
        PREVIOUSLY_SUBMITTED_TO_PAYER = "AB"
        CERTIFICATION_INCLUDED_IN_CLAIM = "AD"
        NARRATIVE_SEGMENT_INCLUDED_IN_CLAIM = "AF"
        NO_DOCUMENTATION_REQUIRED = "AG"
        BY_MAIL = "BM"
        ELECTRONICALLY_ONLY = "EL"
        EMAIL = "EM"
        BY_FAX = "FX"

    report_type_code: AttachmentReportTypeCode
    report_transmission_code: AttachmentTransmissionCode


class Loop2400CrcSegment(CrcSegment):
    """
    Conditions Indicator
    """

    class CodeCategory(str, Enum):
        """
        Code values for CRC01
        """

        AMBULANCE_CERTIFICATION = "07"
        HOSPICE = "70"
        DURABLE_MEDICAL_EQUIPMENT_CERTIFICATION = "09"
        OXYGEN_THERAPY_CERTIFICATION = "11"

    class YesNoResponseCode(str, Enum):
        """
        Code values for CRC
        """

        YES = "Y"
        NO = "N"

    class ConditionsIndicator(str, Enum):
        """
        Code values for CRC03 - CRC07
        """

        # Ambulance Conditions
        PATIENT_ADMITTED_TO_HOSPITAL = "01"
        PATIENT_BED_CONFINED_BEFORE_AMBULANCE = "02"
        PATIENT_BED_CONFINED_AFTER_AMBULANCE = "03"
        PATIENT_MOVED_BY_STRETCHER = "04"
        PATIENT_UNCONSCIOUS_IN_SHOCK = "05"
        PATIENT_EMERGENCY_TRANSPORT = "06"
        PATIENT_RESTRAINED = "07"
        PATIENT_HEMORRHAGING = "08"
        AMBULANCE_MEDICALLY_NECESSARY = "09"
        TRANSPORTATION_NEAREST_FACILITY = "60"
        # Hospice Condition
        OPEN = "65"
        # Durable Medical Equipment Condition
        OXYGEN_DELIVERY_EQUIPMENT_IS_STATIONARY = "37"
        CERTIFICATE_ON_FILE_SUPPLIER = "38"
        AMBULANCE_LIMITATIONS = "AL"
        PATIENT_DISCHARGED_FIRST_FACILITY = "P1"
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
        EXAMINATION = "866"

    date_time_qualifier: DateTimeQualifier


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

    contract_type_code: ContractTypeCode


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
        REFERRAL_NUMBER = "9F"
        PRIOR_AUTHORIZATION_NUMBER = "G1"
        PROVIDER_CONTROL_NUMBER = "6R"
        MAMMOGRAPHY_CERTIFICATION_NUMBER = "EW"
        CLINICAL_LABORATORY_IMPROVEMENT_NUMBER = "X4"
        FACILITY_CERTIFICATION_NUMBER = "F4"
        BATCH_NUMBER = "BT"
        AMBULATORY_PATIENT_GROUP = "1S"
        OXYGEN_FLOW_RATE = "TP"
        PRODUCT_NUMBER = "OZ"
        VENDOR_PRODUCT_NUMBER = "VP"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2400AmtSegment(AmtSegment):
    """
    Loop 2400/Service Line Amounts
    """

    class AmountQualifierCode(str, Enum):
        """
        Code values for AMT01
        """

        GOOD_AND_SERVICES_TAX = "GT"
        MISCELLANEOUS_TAX = "N8"

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

    reference_identification_qualifier: Literal["XZ"]


class Loop2420ANm1Segment(Nm1Segment):
    """
    Loop 2420A Rendering Provider Name
    """

    class IdentificationCodeQualifier(str, Enum):
        """
        Code values for NM108
        """

        EMPLOYER_IDENTIFICATION_NUMBER = "24"
        SOCIAL_SECURITY_NUMBER = "34"
        NATIONAL_PROVIDER_IDENTIFIER = "XX"

    entity_identifier_code: Literal["71"]
    identification_code_qualifier: IdentificationCodeQualifier
    identification_code: str = Field(min_length=2, max_length=80)


class Loop2420APrvSegment(PrvSegment):
    """
    Loop 2420A Rendering Provider Speciality
    """

    provider_code: Literal["PE"]
    reference_identification_qualifier: Literal["ZZ"]


class Loop2420ARefSegment(RefSegment):
    """
    Loop 2420A Rendering Provider Reference Identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        STATE_LICENSE_NUMBER = "0B"
        BLUE_CROSS_PROVIDER_NUMBER = "1A"
        BLUE_SHIELD_PROVIDER_NUMBER = "1B"
        MEDICARE_PROVIDER_NUMBER = "1C"
        MEDICAID_PROVIDER_NUMBER = "1D"
        PROVIDER_UPIN_NUMBER = "1G"
        CHAMPUS_IDENTIFICATION_NUMBER = "1H"
        EMPLOYER_IDENTIFICATION_NUMBER = "EI"
        PROVIDER_COMMERCIAL_NUMBER = "G2"
        LOCATION_NUMBER = "LU"
        PROVIDER_PLAN_NETWORK_IDENTIFIER = "N5"
        SOCIAL_SECURITY_NUMBER = "SY"
        STATE_INDUSTRIAL_ACCIDENT_PROVIDER_NUMBER = "X5"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2420BNm1Segment(Nm1Segment):
    """
    Loop 2420B Purchased Service Provider Name
    """

    class IdentificationCodeQualifier(str, Enum):
        """
        Code values for NM108
        """

        EMPLOYER_IDENTIFICATION_NUMBER = "24"
        SOCIAL_SECURITY_NUMBER = "34"
        NATIONAL_PROVIDER_IDENTIFIER = "XX"

    entity_identifier_code: Literal["72"]
    entity_type_qualifier: Literal["1"]
    identification_code_qualifier: IdentificationCodeQualifier
    identification_code: str = Field(min_length=2, max_length=80)


class Loop2420BRefSegment(RefSegment):
    """
    Loop 2420B Purchased Service Provider Reference Identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        STATE_LICENSE_NUMBER = "0B"
        BLUE_CROSS_PROVIDER_NUMBER = "1A"
        BLUE_SHIELD_PROVIDER_NUMBER = "1B"
        MEDICARE_PROVIDER_NUMBER = "1C"
        MEDICAID_PROVIDER_NUMBER = "1D"
        PROVIDER_UPIN_NUMBER = "1G"
        CHAMPUS_IDENTIFICATION_NUMBER = "1H"
        EMPLOYER_IDENTIFICATION_NUMBER = "EI"
        PROVIDER_COMMERCIAL_NUMBER = "G2"
        LOCATION_NUMBER = "LU"
        PROVIDER_PLAN_NETWORK_IDENTIFIER = "N5"
        SOCIAL_SECURITY_NUMBER = "SY"
        STATE_INDUSTRIAL_ACCIDENT_PROVIDER_NUMBER = "X5"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2420CNm1Segment(Nm1Segment):
    """
    Loop 2420C Other Provider Name
    """

    class IdentificationCodeQualifier(str, Enum):
        """
        Code values for NM108
        """

        EMPLOYER_IDENTIFICATION_NUMBER = "24"
        SOCIAL_SECURITY_NUMBER = "34"
        NATIONAL_PROVIDER_IDENTIFIER = "XX"

    entity_identifier_code: Literal["73"]
    identification_code_qualifier: IdentificationCodeQualifier
    identification_code: str = Field(min_length=2, max_length=80)


class Loop2420CRefSegment(RefSegment):
    """
    Loop 2420C Other Provider Name
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        STATE_LICENSE_NUMBER = "0B"
        BLUE_CROSS_PROVIDER_NUMBER = "1A"
        BLUE_SHIELD_PROVIDER_NUMBER = "1B"
        MEDICARE_PROVIDER_NUMBER = "1C"
        MEDICAID_PROVIDER_NUMBER = "1D"
        PROVIDER_UPIN_NUMBER = "1G"
        CHAMPUS_IDENTIFICATION_NUMBER = "1H"
        EMPLOYERS_IDENTIFICATION_NUMBER = "EI"
        PROVIDER_COMMERCIAL_NUMBER = "G2"
        LOCATION_NUMBER = "LU"
        PROVIDER_PLAN_NETWORK_IDENTIFIER = "N5"
        SOCIAL_SECURITY_NUMBER = "SY"
        STATE_INDUSTRIAL_ACCIDENT_PROVIDER_NUMBER = "X5"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2430DtpSegment(DtpSegment):
    """
    Loop 2430 Line Check or Remittance Date
    """

    date_time_qualifier: Literal["573"]
    date_time_period_format_qualifier: Literal["D8"]
