"""
segments.py

Specialized segment models for the Eligibility 270 005010X279A1 transaction.
"""
from enum import Enum
from typing import Literal, Optional, List

from pydantic import Field
from linuxforhealth.x12.v5010.validators import validate_hl_parent_id
from linuxforhealth.x12.v5010.segments import (
    BhtSegment,
    HlSegment,
    Nm1Segment,
    StSegment,
    PrvSegment,
    DtpSegment,
    RefSegment,
    InsSegment,
    EqSegment,
    IiiSegment,
    AmtSegment,
)


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

    hierarchical_structure_code: Literal["0022"]
    transaction_set_purpose_code: PurposeCode
    submitter_transactional_identifier: str = Field(min_length=1, max_length=50)
    transaction_type_code: Optional[Literal["RT"]]


class Loop2000AHlSegment(HlSegment):
    """
    Loop2000A HL segment adjusted for Information Source usage
    """

    hierarchical_parent_id_number: Optional[str]
    hierarchical_level_code: Literal["20"]
    hierarchical_child_code: Literal["1"]

    _parent_id_validator = validate_hl_parent_id


class Loop2100ANm1Segment(Nm1Segment):
    """
    Loop 2100A NM1 segment adjusted for Information Source usage
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


class Loop2000BHlSegment(HlSegment):
    """
    Loop2000B HL segment adjusted for Information Receiver usage
    """

    hierarchical_level_code: Literal["21"]
    hierarchical_child_code: Literal["1"]


class Loop2100BNm1Segment(Nm1Segment):
    """
    Loop2000B (Information Receiver) Nm1 Segment requires identification code qualifier and value (NM108 and NM109)
    """

    class EntityIdentifierCode(str, Enum):
        """
        Code value for NM101
        """

        PROVIDER = "1P"
        THIRD_PARTY_ADMINISTRATOR = "2B"
        EMPLOYER = "36"
        HOSPITAL = "80"
        FACILITY = "FA"
        GATEWAY_PROVIDER = "GP"
        PLAN_SPONSOR = "P5"
        PAYOR = "PR"

    class IdentificationCodeQualifier(str, Enum):
        """
        Code value for NM108
        """

        EMPLOYER_IDENTIFICATION_NUMBER = "24"
        SOCIAL_SECURITY_NUMBER = "34"
        FEDERAL_TAXPAYER_IDENTIFICATION_NUMBER = "FI"
        PAYOR_IDENTIFICATION = "PI"
        PHARMACY_PROCESSOR_NUMBER = "PP"
        SERVICE_PROVIDER_NUMBER = "SV"
        MEDICARE_MEDICAID_PLAN_ID = "XV"
        MEDICARE_MEDICAID_NATIONAL_PROVIDER_ID = "XX"

    entity_identifier_code: EntityIdentifierCode
    identification_code_qualifier: IdentificationCodeQualifier
    identification_code: str


class Loop2100BRefSegment(RefSegment):
    """
    Information Receiver Additional Identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        STATE_LICENSE_NUMBER = "0B"
        MEDICARE_PROVIDER_NUMBER = "1C"
        MEDICAID_PROVIDER_NUMBER = "1D"
        FACILITY_ID_NUMBER = "1J"
        PERSONAL_IDENTIFICATION_NUMBER = "4A"
        CONTRACT_NUMBER = "CT"
        ELECTRONIC_DEVICE_PIN_NUMBER = "EL"
        SUBMITTER_IDENTIFICATION_NUMBER = "EO"
        NATIONAL_PROVIDER_IDENTIFIER = "HPI"
        USER_IDENTIFICATION = "JD"
        PROVIDER_PLAN_NETWORK_IDENTIFICATION_NUMBER = "N5"
        FACILITY_NETWORK_IDENTIFICATION_NUMBER = "N7"
        PRIOR_IDENTIFIER_NUMBER = "Q4"
        SOCIAL_SECURITY_NUMBER = "SY"
        FEDERAL_TAXPAYER_IDENTIFICATION_NUMBER = "TJ"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2100BPrvSegment(PrvSegment):
    """
    Additional provider information for Information Receiver.
    """

    class ProviderCode(str, Enum):
        """
        PRV01 code value
        """

        ADMITTING = "AD"
        ATTENDING = "AT"
        BILLING = "BI"
        CONSULTING = "CO"
        COVERING = "CV"
        HOSPITAL = "H"
        HOME_HEALTH_CARE = "HH"
        LABORATORY = "LA"
        OTHER_PHYSICIAN = "OT"
        PHARMACIST = "P1"
        PHARMACY = "P2"
        PRIMARY_CARE_PHYSICIAN = "PC"
        PERFORMING = "PE"
        RURAL_HEALTH_CLINIC = "R"
        REFERRING = "RF"
        SUBMITTING = "SB"
        SKILLED_NURSING_FACILITY = "SK"
        SUPERVISING = "SU"

    provider_code: ProviderCode


class Loop2000CHlSegment(HlSegment):
    """
    Loop2000C HL segment adjusted for Subscriber usage
    """

    hierarchical_level_code: Literal["22"]


class Loop2100CNm1Segment(Nm1Segment):
    """
    Loop 2100C NM1 segment for Subscriber name.
    """

    entity_identifier_code: Literal["IL"]
    name_last_or_organization_name: Optional[str]


class Loop2100RefSegment(RefSegment):
    """
    Conveys additional Subscriber or Dependent identification data.
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        PLAN_NUMBER = "18"
        GROUP_POLICY_NUMBER = "1L"
        MEMBER_IDENTIFICATION_NUMBER = "1W"
        CASE_NUMBER = "3H"
        GROUP_NUMBER = "6P"
        CONTRACT_NUMBER = "CT"
        MEDICAL_RECORD_IDENTIFICATION_NUMBER = "EA"
        PATIENT_ACCOUNT_NUMBER = "EJ"
        HEALTH_INSURANCE_CLAIM_NUMBER = "F6"
        IDENTIFICATION_CARD_SERIAL_NUMBER = "GH"
        IDENTITY_CARD_NUMBER = "HJ"
        INSURANCE_POLICY_NUMBER = "IG"
        PLAN_NETWORK_IDENTIFICATION_NUMBER = "N6"
        MEDICARE_RECIPIENT_IDENTIFICATION_NUMBER = "NQ"
        SOCIAL_SECURITY_NUMBER = "SY"
        AGENCY_CLAIM_NUMBER = "Y4"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2100CPrvSegment(Loop2100BPrvSegment):
    """
    Associates a specific provider to the subscriber/member
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for PRV02
        """

        SERVICER = "9K"
        PRESCRIPTION_DRUG_PROGRAMS_PHARMACY_NUMBER = "D3"
        EMPLOYER_IDENTIFICATION_NUMBER = "EI"
        NATIONAL_PROVIDER_IDENTIFIER = "HPI"
        HEALTH_CARE_PROVIDER_TAXONOMY_CODE = "PXC"
        SOCIAL_SECURITY_NUMBER = "SY"
        FEDERAL_TAXPAYER_IDENTIFICATION_NUMBER = "TJ"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2100CInsSegment(InsSegment):
    """
    Used if the subscriber falls within a "multiple birth" condition and cannot be resolved using a lookup by name
    and birth date.
    """

    member_indicator: Literal["Y"]
    individual_relationship_code: Literal["18"]
    maintenance_type_code: Optional[str]
    benefit_status_code: Optional[str]


class Loop2100DtpSegment(DtpSegment):
    """
    Loop 2100C STP segment for Subscriber date/date ranges.
    """

    class DateTimeQualifier(str, Enum):
        """
        Code values for DTP01
        """

        ISSUE = "102"
        PLAN = "291"

    date_time_qualifier: DateTimeQualifier


class Loop2110EqSegment(EqSegment):
    """
    Loop2110C EQ segment for subscriber eligibility inquiry.
    """

    class ServiceTypeCode(str, Enum):
        """
        Code values for EQ01
        """

        MEDICAL_CARE = "1"
        SURGICAL = "2"
        CONSULTATION = "3"
        DIAGNOSTIC_XRAY = "4"
        DIAGNOSTIC_LAB = "5"
        RADIATION_THERAPY = "6"
        ANESTHESIA = "7"
        SURGICAL_ASSISTANCE = "8"
        OTHER_MEDICAL = "9"
        BLOOD_CHARGES = "10"
        USED_DURABLE_MEDICAL_EQUIPMENT = "11"
        DURABLE_MEDICAL_EQUIPMENT_PURCHASE = "12"
        AMBULATORY_SERVICE_CENTER_FACILITY = "13"
        RENAL_SUPPLIES_IN_HOME = "14"
        ALTERNATE_METHOD_DIALYSIS = "15"
        CHRONIC_RENAL_DISEASE_EQUIPMENT = "16"
        PRE_ADMISSION_TESTING = "17"
        DURABLE_MEDICAL_EQUIPMENT_RENTAL = "18"
        PNEUMONIA_VACCINE = "19"
        SECOND_SURGICAL_OPINION = "20"
        THIRD_SURGICAL_OPINION = "21"
        SOCIAL_WORK = "22"
        DIAGNOSTIC_DENTAL = "23"
        PERIODONTICS = "24"
        RESTORATIVE = "25"
        ENDODONTICS = "26"
        MAXOILLOFACIAL_PROSETHETICS = "27"
        ADJUNCTIVE_DENTAL_SERVICES = "28"
        HEALTH_BENEFIT_PLAN_COVERAGE = "30"
        PLAN_WAITING_PERIOD = "32"
        CHIROPRACTIC = "33"
        CHIROPRACTIC_OFFICE_VISITS = "34"
        DENTAL_CARE = "35"
        DENTAL_CROWNS = "36"
        DENTAL_ACCIDENT = "37"
        ORTHODONTICS = "38"
        PROSTHODONTICS = "39"
        ORAL_SURGERY = "40"
        ROUTINE_PREVENTATIVE_DENTAL = "41"
        HOME_HEALTH_CARE = "42"
        HOME_HEALTH_PRESCRIPTIONS = "43"
        HOME_HEALTH_VISITS = "44"
        HOSPICE = "45"
        RESPITE_CARE = "46"
        HOSPITAL = "47"
        HOSPITAL_INPATIENT = "48"
        HOSPITAL_ROOM_AND_BOARD = "49"
        HOSPITAL_OUTPATIENT = "50"
        HOSPITAL_EMERGENCY_ACCIDENT = "51"
        HOSPITAL_EMERGENCY_MEDICAL = "52"
        HOSPITAL_AMBULATORY_SURGICAL = "53"
        LONG_TERM_CARE = "54"
        MAJOR_MEDICAL = "55"
        MEDICALLY_RELATED_TRANSPORTATION = "56"
        AIR_TRANSPORTATION = "57"
        CABULANCE = "58"
        LICENSED_AMBULANCE = "59"
        GENERAL_BENEFITS = "60"
        INVITRO_FERTILIZATION = "61"
        MRI_CAT_SCAN = "62"
        DONOR_PROCEDURES = "63"
        ACUPUNCTURE = "64"
        NEWBORN_CARE = "65"
        PATHOLOGY = "66"
        SMOKING_CESSATION = "67"
        WELL_BABY_CARE = "68"
        MATERNITY = "69"
        TRANSPLANTS = "70"
        AUDIOLOGY_EXAM = "71"
        INHALATION_THERAPY = "72"
        DIAGNOSTIC_MEDICAL = "73"
        PRIVATE_DUTY_NURSING = "74"
        PROSTHETIC_DEVICE = "75"
        DIALYSIS = "76"
        OTOLOGICAL_EXAM = "77"
        CHEMOTHERAPY = "78"
        ALLERGY_TESTING = "79"
        IMMUNIZATIONS = "80"
        ROUTINE_PHYSICAL = "81"
        FAMILY_PLANNING = "82"
        INFERTILITY = "83"
        ABORTION = "84"
        AIDS = "85"
        EMERGENCY_SERVICES = "86"
        CANCER = "87"
        PHARMACY = "88"
        FREE_STANDING_PRESCRIPTION_DRUG = "89"
        MAIL_ORDER_PRESCRIPTION_DRUG = "90"
        BRAND_NAME_PRESCRIPTION_DRUG = "91"
        GENERIC_PRESCRIPTION_DRUG = "92"
        PODIATRY = "93"
        PODIATRY_OFFICE_VISITS = "94"
        PODIATRY_NURSING_HOME_VISITS = "95"
        PROFESSIONAL_PHYSICIAN = "96"
        ANESTHESIOLOGIST = "97"
        PROFESSIONAL_PHYSICIAN_VISIT_OFFICE = "98"
        PROFESSIONAL_PHYSICIAN_VISIT_INPATIENT = "99"
        PROFESSIONAL_PHYSICIAN_VISIT_OUTPATIENT = "A0"
        PROFESSIONAL_PHYSICIAN_VISIT_NURSING_HOME = "A1"
        PROFESSIONAL_PHYSICIAN_VISIT_SKILLED_NURSING_FACILITY = "A2"
        PROFESSIONAL_PHYSICIAN_VISIT_HOME = "A3"
        PSYCHIATRIC = "A4"
        PSYCHIATRIC_ROOM_AND_BOARD = "A5"
        PSYCHOTHERAPY = "A6"
        PSYCHIATRIC_INPATIENT = "A7"
        PSYCHIATRIC_OUTPATIENT = "A8"
        REHABILITATION = "A9"
        REHABILITATION_ROOM_AND_BOARD = "AA"
        REHABILITATION_INPATIENT = "AB"
        REHABILITATION_OUTPATIENT = "AC"
        OCCUPATIONAL_THERAPY = "AD"
        PHYSICAL_MEDICINE = "AE"
        SPEECH_THERAPY = "AF"
        SKILLED_NURSING_CARE = "AG"
        SKILLED_NURSING_CARE_ROOM_AND_BOARD = "AH"
        SUBSTANCE_ABUSE = "AI"
        ALCOHOLISM = "AJ"
        DRUG_ADDICTION = "AK"
        VISION_OPTOMETRY = "AL"
        FRAMES = "AM"
        ROUTINE_EXAM = "AN"
        LENSES = "AO"
        NONMEDICAL_NECESSARY_PHYSICAL = "AQ"
        EXPERIMENTAL_DRUG_THERAPY = "AR"
        BURN_CARE = "B1"
        BRAND_NAME_PRESCRIPTION_DRUG_FORMULARY = "B2"
        BRAND_NAME_PRESCRIPTION_DRUG_NON_FORMULARY = "B3"
        INDEPENDENT_MEDICAL_EVALUATION = "BA"
        PARTIAL_HOSPITALIZATION_PSYCHIATRIC = "BB"
        DAY_CARE_PSYCHIATRIC = "BC"
        COGNITIVE_THERAPY = "BD"
        MESSAGE_THERAPY = "BE"
        PULMONARY_REHABILITATION = "BF"
        CARDIAC_REHABILITATION = "BG"
        PEDIATRIC = "BH"
        NURSERY = "BI"
        SKIN = "BJ"
        ORTHOPEDIC = "BK"
        CARDIAC = "BL"
        LYMPHATIC = "BM"
        GASTROINSTESTINAL = "BN"
        ENDOCRINE = "BP"
        NEUROLOGY = "BQ"
        EYE = "BR"
        INVASIVE_PROCEDURES = "BS"
        GYNECOLOGICAL = "BT"
        OBSTETRICAL = "BU"
        OBSTETRICAL_GYNECOLOGICAL = "BV"
        MAIL_ORDER_PRESCRIPTION_DRUG_BRAND_NAME = "BW"
        MAIL_ORDER_PRESCRIPTION_DRUG_GENERIC = "BX"
        PHYSICIAN_VISIT_OFFICE_SICK = "BY"
        PHYSICIAN_VISIT_OFFICE_WELL = "BZ"
        CORONARY_CARE = "C1"
        PRIVATE_DUTY_NURSING_INPATIENT = "CA"
        PRIVATE_DUTY_NURSING_HOME = "CB"
        SURGICAL_BENEFITS_PROFESSIONAL_PHYSICIAN = "CC"
        SURGICAL_BENEFITS_FACILITY = "CD"
        MENTAL_HEALTH_PROVIDER_INPATIENT = "CE"
        MENTAL_HEALTH_PROVIDER_OUTPATIENT = "CF"
        MENTAL_HEALTH_FACILITY_INPATIENT = "CG"
        MENTAL_HEALTH_FACILITY_OUTPATIENT = "CH"
        SUBSTANCE_ABUSE_FACILITY_INPATIENT = "CI"
        SUBSTANCE_ABUSE_FACILITY_OUTPATIENT = "CJ"
        SCREENING_XRAY = "CK"
        SCREENING_LABORATORY = "CL"
        MAMMOGRAM_HIGH_RISK_PATIENT = "CM"
        MAMMOGRAM_LOW_RISK_PATIENT = "CN"
        FLU_VACCINATION = "CO"
        EYEWEAR_AND_EYEWEAR_ACCESSORIES = "CP"
        CASE_MAANGEMENT = "CQ"
        DERMATOLOGY = "DG"
        DURABLE_MEDICAL_EQUIPMENT = "DM"
        DIABETIC_SUPPLIES = "DS"
        GENERIC_PRESCRIPTION_DRUG_FORMULARY = "GF"
        GENERIC_PRESCRIPTION_DRUG_NON_FORMULARY = "GN"
        ALLERGY = "GY"
        INTENSIVE_CARE = "IC"
        MENTAL_HEALTH = "MH"
        NEONATAL_INTENSIVE_CARE = "NI"
        ONCOLOGY = "ON"
        PHYSICAL_THERAPY = "PT"
        PULMONARY = "PU"
        RENAL = "RN"
        RESIDENTIAL_PSYCHIATRIC_TREATMENT = "RT"
        TRANSITIONAL_CARE = "TC"
        TRANSITIONAL_NURSERY_CARE = "TN"
        URGENT_CARE = "UC"

    service_type_code: List[ServiceTypeCode]


class Loop2110AmtSegment(AmtSegment):
    """
    Used if it is necessary to report the amount applied towards the deductible.
    Used for Subscriber and Dependent 2110 loops.
    """

    class AmountQualifierCode(str, Enum):
        """
        Code values for AMT01
        """

        SPEND_DOWN = "R"
        BILLED_AMOUNT = "PB"

    amount_qualifier_code: AmountQualifierCode


class Loop2110IiiSegment(IiiSegment):
    """
    Used for Subscriber and Dependent 2110 loops.
    """

    class IndustryCode(str, Enum):
        """
        Code values for III02
        """

        PHARMACY = "01"
        SCHOOL = "03"
        HOMELESS_SHELTER = "04"
        INDIAN_HEALTH_SERVICE_FREE_STANDING_FACILITY = "05"
        INDIAN_HEALTH_SERVICE_PROVIDER_BASED_FACILITY = "06"
        TRIBAL_638_FREE_STANDING_FACILITY = "07"
        TRIBAL_638_PROVIDER_BASED_FACILITY = "08"
        OFFICE = "11"
        HOME = "12"
        ASSISTED_LIVING_FACILITY = "13"
        GROUP_HOME = "14"
        MOBILE_UNIT = "15"
        URGENT_CARE_FACILITY = "20"
        INPATIENT_HOSPITAL = "21"
        OUTPATIENT_HOSPITAL = "22"
        EMERGENCY_ROOM_HOSPITAL = "23"
        AMBULATORY_SURGICAL_CENTER = "24"
        BIRTHING_CENTER = "25"
        MILITARY_TREATMENT_FACILITY = "26"
        SKILLED_NURSING_FACILITY = "31"
        NURSING_FACILITY = "32"
        CUSTODIAL_CARE_FACILITY = "33"
        HOSPICE = "34"
        AMBULANCE_LAND = "31"
        AMBULANCE_AIR_OR_WATER = "42"
        INDEPENDENT_CLINIC = "49"
        FEDERALLY_QUALIFIED_HEALTH_CENTER = "50"
        INPATIENT_PSYCHIATRIC_FACILITY = "51"
        PSYCHIATRIC_FACILITY_PARTIAL_HOSPITALIZATION = "52"
        COMMUNITY_MENTAL_HEALTH_CENTER = "53"
        INTERMEDIATE_CARE_FACILITY_MENTALLY_RETARDED = "54"
        RESIDENTIAL_SUBSTANCE_ABUSE_TREATMENT_FACILITY = "55"
        PSYCHIATRIC_RESIDENTIAL_TREATMENT_CENTER = "56"
        NONRESIDENTIAL_SUBSTANCE_TREATMENT_FACILITY = "57"
        MASS_IMMUNIZATION_CENTER = "60"
        COMPREHENSIVE_INPATIENT_REHABILITATION_FACILITY = "61"
        COMPREHENSIVE_OUTPATIENT_REHABILITATION_FACILITY = "62"
        END_STAGE_RENAL_DISEASE_TREATMENT_FACILITY = "65"
        PUBLIC_HEALTH_CLINIC = "71"
        RURAL_HEALTH_CLINIC = "72"
        INDEPENDENT_LABORATORY = "81"
        OTHER_PLACE_OF_SERVICE = "99"

    code_list_qualifier_code: Literal["ZZ"]
    industry_code: IndustryCode


class Loop2110RefSegment(RefSegment):
    """
    Conveys referral or prior authorization information, if needed for a Subscriber or Dependent loop.
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        REFERRAL_NUMBER = "9F"
        PRIOR_AUTHORIZATION_NUMBER = "G1"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2110DtpSegment(DtpSegment):
    """
    Overrides dates in Loop2100C to support an eligibility inquiry for a specific date or date range.
    """

    date_time_qualifier: Literal["291"]


class Loop2000DHlSegment(HlSegment):
    """
    Loop2000C HL segment adjusted for Subscriber usage
    """

    hierarchical_level_code: Literal["23"]


class Loop2100DNm1Segment(Nm1Segment):
    """
    Loop 2100D NM1 segment for Dependent name.
    """

    entity_identifier_code: Literal["03"]
    name_first: str
    identification_code_qualifier: Optional[str]
    identification_code: Optional[str]


class Loop2100DInsSegment(InsSegment):
    """
    Used if the dependent falls within a "multiple birth" condition and cannot be resolved using a lookup by name
    and birth date.
    """

    class IndividualRelationshipCode(str, Enum):
        """
        Code values for INS02
        """

        SPOUSE = "01"
        CHILD = "19"
        OTHER_CHILD = "34"

    member_indicator: Literal["N"]
    individual_relationship_code: IndividualRelationshipCode
    maintenance_type_code: Optional[str]
    benefit_status_code: Optional[str]
