"""
segments.py

The segments module contains models for ALL ASC X12 segments used within health care transactions.
The segments defined within this module serve as "base models" for transactional use, where a segment subclass is defined
and overriden as necessary to support a transaction's specific validation and usage constraints.
"""

import datetime
from enum import Enum
from typing import Dict, List, Literal, Optional, Tuple, Union
from decimal import Decimal

from pydantic import Field, PositiveInt, condecimal, validator, root_validator

from x12.models import X12Segment, X12SegmentName
from x12.support import (
    parse_x12_date,
    parse_x12_time,
    parse_interchange_date,
    field_validator,
)
from x12.validators import validate_date_field


class AaaSegment(X12Segment):
    """
    Request validation.
    Example:
        AAA*Y**42*Y~
    """

    class ResponseCode(str, Enum):
        """
        AAA01 code values
        """

        NO = "N"
        YES = "Y"

    segment_name: X12SegmentName = X12SegmentName.AAA
    response_code: ResponseCode
    agency_qualifier_code: Optional[str]
    reject_reason_code: str
    follow_up_action_code: str


class AmtSegment(X12Segment):
    """
    Monetary Amount Information.
    Example:
        AMT*R*37.5~
    """

    segment_name: X12SegmentName = X12SegmentName.AMT
    amount_qualifier_code: str = Field(min_length=1, max_length=3)
    monetary_amount: condecimal(ge=Decimal("0.00"))
    credit_debit_flag_code: Optional[str]


class BhtSegment(X12Segment):
    """
    Defines the business application purpose and supporting reference data for the transaction.
    Example:
        BHT*0022*01**19980101*1400*RT~
    """

    segment_name: X12SegmentName = X12SegmentName.BHT
    hierarchical_structure_code: str = Field(min_length=4, max_length=4)
    transaction_set_purpose_code: str = Field(min_length=2, max_length=2)
    submitter_transactional_identifier: str = Field(min_length=1, max_length=50)
    transaction_set_creation_date: Union[str, datetime.date]
    transaction_set_creation_time: Union[str, datetime.time]
    transaction_type_code: str = Field(min_length=2, max_length=2)

    _validate_transaction_date = field_validator("transaction_set_creation_date")(
        parse_x12_date
    )
    _validate_transaction_time = field_validator("transaction_set_creation_time")(
        parse_x12_time
    )


class DmgSegment(X12Segment):
    """
    Demographic Information (birthdate, gender).
    Example:
        DMG*D8*19430917*M~
    """

    class GenderCode(str, Enum):
        """
        Code value for DMG03
        """

        FEMALE = "F"
        MALE = "M"

    class DateTimePeriodFormatQualifier(str, Enum):
        """
        Code value for DMG01
        """

        SPECIFIC_DATE = "D8"

    segment_name: X12SegmentName = X12SegmentName.DMG
    date_time_period_format_qualifier: Optional[DateTimePeriodFormatQualifier]
    date_time_period: Optional[Union[str, datetime.date]]
    gender_code: Optional[GenderCode]

    _validate_x12_date = field_validator("date_time_period")(validate_date_field)

    @root_validator
    def validate_date_time_fields(cls, values):
        """
        Validates that both a date_time_period_format_qualifier and date_time_period are provided if one or the other is present

        :param values: The raw, unvalidated transaction data.
        """
        date_fields: Tuple = values.get(
            "date_time_period_format_qualifier"
        ), values.get("date_time_period")

        if any(date_fields) and not all(date_fields):
            raise ValueError(
                "DMG Segment requires both a date_time_period_format_qualifier and date time period if one or the other is present"
            )

        return values


class DtpSegment(X12Segment):
    """
    Date or Time Period
    Example:
        DTP*291*D8*20051015~
    """

    class DateTimePeriodFormatQualifier(str, Enum):
        """
        Code values for DTP02
        """

        SPECIFIC_DATE = "D8"
        DATE_RANGE = "RD8"

    segment_name: X12SegmentName = X12SegmentName.DTP
    date_time_qualifier: str = Field(min_length=3, max_length=3)
    date_time_period_format_qualifier: DateTimePeriodFormatQualifier
    date_time_period: Union[str, datetime.date]

    _validate_x12_date = field_validator("date_time_period")(validate_date_field)


class EbSegment(X12Segment):
    """
    Eligibility Benefit Information
    Example:
        EB*B**1^33^35^47^86^88^98^AL^MH^UC*HM*GOLD 123 PLAN*27*10*****Y~
    """

    class EligibilityBenefitInformationCode(str, Enum):
        """
        Code values for EB01
        """

        ACTIVE_COVERAGE = "1"
        ACTIVE_FULL_RISK_CAPITATION = "2"
        ACTIVE_SERVICES_CAPITATED = "3"
        ACTIVE_SERVICES_CAPITATED_TO_PRIMARY_CARE = "4"
        ACTIVE_PENDING_INVESTIGATION = "5"
        INACTIVE = "6"
        INACTIVE_PENDING_ELIGIBILITY_UPDATE = "7"
        INACTIVE_PENDING_INVESTIGATION = "8"
        CO_INSURANCE = "A"
        CO_PAYMENT = "B"
        DEDUCTIBLE = "C"
        COVERAGE_BASIS = "CB"
        BENEFIT_DESCRIPTION = "D"
        EXCLUSIONS = "E"
        LIMITATIONS = "F"
        OUT_OF_POCKET_STOP_LOSS = "G"
        UNLIMITED = "H"
        NON_COVERED = "I"
        COST_CONTAINMENT = "J"
        REVERSE = "K"
        PRIMARY_CARE_PROVIDER = "L"
        PRE_EXISTING_CONDITION = "M"
        MANAGED_CARE_COORDINATOR = "MC"
        SERVICES_RESTRICTED_TO_FOLLOWING_PROVIDER = "N"
        NOT_DEEMED_A_MEDICAL_NECESSITY = "O"
        BENEFIT_DISCLAIMER = "P"
        SECOND_SURGICAL_OPINION_REQUIRED = "Q"
        OTHER_OR_ADDITIONAL_PAYOR = "R"
        PRIOR_YEAR_HISTORY = "S"
        CARD_REPORTED_LOST_STOLEN = "T"
        CONTACT_FOLLOWING_FOR_BENEFIT_INFO = "U"
        CANNOT_PROCESS = "V"
        OTHER_SOURCE_OF_DATA = "W"
        HEALTH_CARE_FACILITY = "X"
        SPEND_DOWN = "Y"

    class CoverageLevelCode(str, Enum):
        """
        Code values for EB02
        """

        CHILDREN_ONLY = "CHD"
        DEPENDENTS_ONLY = "DEP"
        EMPLOYEE_AND_CHILDREN = "ECH"
        EMPLOYEE_ONLY = "EMP"
        EMPLOYEE_AND_SPOUSE = "ESP"
        FAMILY = "FAM"
        INDIVIDUAL = "IND"
        SPOUSE_AND_CHILDREN = "SPC"
        SPOUSE_ONLY = "SPO"

    class ServiceTypeCode(str, Enum):
        """
        Code values for EB03
        """

        MEDICAL_CARE = "1"
        SURGICAL = "2"
        CONSULTATION = "3"
        DIAGNOSTIC_X_RAY = "4"
        DIAGNOSTIC_LAB = "5"
        RADIATION_THERAPY = "6"
        ANESTHESIA = "7"
        SURGICAL_ASSISTANCE = "8"
        OTHER_MEDICAL = "9"
        BLOOD_CHARGES = "10"
        USED_DURABLE_MEDICAL_EQUIPMENT = "11"
        DURABLE_MEDICAL_EQUIPMENT_PURCHASE = "12"
        AMBULATORY_SERVICE_CENTER_FACILITY = "13"
        RENAL_SUPPLIES_IN_THE_HOME = "14"
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
        MAXILLOFACIAL_PROSTHETICS = "27"
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
        ROUTINE_PREVENTIVE_DENTAL = "41"
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
        DONOR_PROCEDURE = "63"
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
        PDDIATRY = "93"
        PDDIATRY_NURSING_HOME_VISITS = "94"
        PROFESSIONAL_PHYSICIAN = "96"
        ANESTHESIOLOGIST = "97"
        PROFESSIONAL_PHYSICIAN_VISIT_OFFICE = "98"
        PROFESSIONAL_PHYSICIAN_VISIT_INPATIENT = "99"
        PROFESSIONAL_PHYSICIAN_VISIT_OUTPATIENT = "99"
        PROFESSIONAL_PHYSICIAN_VISIT_NURSING_HOME = "A1"
        PROFESSIONAL_PHYSICIAN_VISIT_SKILLED_NURSING_FACILITY = "A2"
        PROFESSIONAL_PHYSICIAN_VISIT_HOME_PSYCHIATRIC = "A3"
        PSYCHIATRIC_ROOM_AND_BOARD = "A4"
        PSYCHOTHERAPY = "A5"
        PSYCHIATRIC_INPATIENT = "A6"
        PSYCHIATRIC_OUTPATIENT = "A7"
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
        ROUTINE_VISION_EXAM = "AN"
        LENSES = "AO"
        NONMEDICALLY_NECESSARY_PHYSICAL = "AQ"
        EXPERIMENTAL_DRUG_THERAPY = "AR"
        BURN_CARE = "B1"
        BRAND_NAME_PRESCRIPTION_DRUG_FORMULARY = "B2"
        BRAND_NAME_PRESCRIPTION_DRUG_NON_FORMULARY = "B3"
        INDEPENDENT_MEDICAL_EVALUATION = "BA"
        PARTIAL_HOSPITALIZATION_PSYCHIATRIC = "BB"
        DAY_CARE_PSYCHIATRIC = "BC"
        COGNITIVE_THERAPY = "BD"
        MASSAGE_THERAPY = "BE"
        PULMONARY_REHABILITATION = "BF"
        CARDIAC_REHABILITATION = "BG"
        PEDIATRIC = "BH"
        NURSERY = "BI"
        SKIN = "BJ"
        ORTHOPEDIC = "BK"
        CARDIAC = "BL"
        LYMPHATIC = "BM"
        GASTROINTESTINAL = "BN"
        ENDOCRINE = "BP"
        NEUROLOGY = "BQ"
        EYE = "BR"
        INVASIVE_PROCEDURE = "BS"
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
        SUBSTANCE_ABUSE_FACILITY_INPATIENT = "C1"
        SUBSTANCE_ABUSE_FACILITY_OUTPATIENT = "C2"
        SCREENING_X_RAY = "CK"
        SCREENING_LABORATORY = "CL"
        MAMMOGRAM_HIGH_RISK_PATIENT = "CM"
        MAMMOGRAM_LOW_RISK_PATIENT = "CN"
        FLU_VACCINATION = "CO"
        EYEWEAR_AND_EYEWEAR_ACCESSORIES = "CP"
        CASE_MANAGEMENT = "CQ"
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
        TRANSITION_NURSERY_CARE = "TN"
        URGENT_CARE = "UC"

    class InsuranceTypeCode(str, Enum):
        """
        code values for EB04
        """

        MEDICARE_SECONDARY_EMPLOYER_GROUP_PRIMARY = "12"
        MEDICARE_SECONDARY_END_STAGE_RENAL_DISEASE = "13"
        MEDICARE_SECONDARY_AUTO_PRIMARY = "14"
        MEDICARE_SECONDARY_WORKERS_COMP = "15"
        MEDICARE_SECONDARY_PUBLIC_HEALTH_SERVICE = "16"
        MEDICARE_SECONDARY_BLACK_LUNG = "41"
        MEDICARE_SECONDARY_VETERANS_ADMIN = "42"
        MEDICARE_SECONDARY_DISABLED_BENEFICIARY = "43"
        MEDICARE_SECONDARY_OTHER_LIABILITY = "47"
        AUTO_INSURANCE_POLICY = "AP"
        COMMERCIAL = "C1"
        COBRA = "CO"
        MEDICARE_CONDITIONALLY_PRIMARY = "CP"
        DISABILITY = "D"
        DISABILITY_BENEFITS = "DB"
        EXCLUSIVE_PROVIDER_ORGANIZATION = "EP"
        FAMILY_OR_FRIENDS = "FF"
        GROUP_POLICY = "GP"
        HMO = "HM"
        HMO_MEDICARE_RISK = "HN"
        SPECIAL_LOW_INCOME_MEDICARE_BENEFICIARY = "HS"
        INDEMNITY = "IN"
        INDIVIDUAL_POLICY = "IP"
        LONG_TERM_CARE = "LC"
        LONG_TERM_POLICY = "LD"
        LIFE_INSURANCE = "LI"
        LITIGATION = "LT"
        MEDICARE_PART_A = "MA"
        MEDICARE_PART_B = "MB"
        MEDICAID = "MC"
        MEDIGAP_PART_A = "MH"
        MEDIGAP_PART_B = "MI"
        MEDICARE_PRIMARY = "MP"
        OTHER = "OT"
        PROPERTY_INSURANCE_PERSONAL = "PE"
        PERSONAL = "PL"
        PERSONAL_PAYMENT_CASH = "PP"
        PREERRED_PROVIDER_ORGANIZATION = "PR"
        POINT_OF_SERVICE = "POS"
        QUALIFIED_MEDICARE_BENEFICIARY = "QM"
        PROPERTY_INSURANCE_REAL = "RP"
        SUPPLEMENTAL_POLICY = "SP"
        TEFRA = "TF"
        WORKERS_COMPENSATION = "WC"
        WRAP_UP_POLICY = "WU"

    class TimePeriodQualifier(str, Enum):
        """
        Code values for EB06
        """

        HOUR = "6"
        DAY = "7"
        TWENTY_FOUR_HOURS = "13"
        YEARS = "21"
        SERVICE_YEAR = "22"
        CALENDAR_YEAR = "23"
        YEAR_TO_DATE = "24"
        CONTRACT = "25"
        EPISODE = "26"
        VISIT = "27"
        OUTLIER = "28"
        REMAINING = "29"
        EXCEEDED = "30"
        NOT_EXCEEDED = "31"
        LIFETIME = "32"
        LIFETIME_REMAINING = "33"
        MONTH = "34"
        WEEK = "35"
        ADMISSION = "36"

    class QuantityQualifier(str, Enum):
        """
        Code valus for EB09
        """

        MINIMUM = "8H"
        QUANTITY_USED = "99"
        COVERED_ACTUAL = "CA"
        COVERED_ESTIMATED = "CE"
        NUMBER_OF_COINSURANCE_DAYS = "D3"
        DEDUCTIBLE_BLOOD_UNITS = "D8"
        DAYS = "DY"
        HOURS = "HS"
        LIFETIME_RESERVE_ACTUAL = "LA"
        LIFETIME_RESERVE_ESTIMATED = "LE"
        MAXIMUM = "M2"
        MONTH = "MN"
        NUMBER_OF_SERVICES_OR_PROCEDURES = "P6"
        QUANTITY_APPROVED = "QA"
        AGE_HIGH_VALUE = "S7"
        AGE_LOW_VALUE = "S8"
        VISITS = "VS"
        YEARS = "YY"

    class AuthorizationCertificationIndicator(str, Enum):
        """
        Code values for EB11
        """

        NO = "N"
        UNKNOWN = "U"
        YES = "Y"

    class InPlanNetworkIndicator(str, Enum):
        """
        Code values for EB12
        """

        NO = "N"
        UNKNOWN = "U"
        NOT_APPLICABLE = "W"
        YES = "Y"

    segment_name: X12SegmentName = X12SegmentName.EB
    eligibility_benefit_information: EligibilityBenefitInformationCode
    coverage_level_code: Optional[CoverageLevelCode]
    service_type_code: Optional[List[ServiceTypeCode]]
    insurance_type_code: Optional[InsuranceTypeCode]
    plan_coverage_description: Optional[str]
    time_period_qualifier: Optional[TimePeriodQualifier]
    benefit_amount: Optional[Decimal]
    benefit_percent: Optional[Decimal]
    quantity_qualifier: Optional[Decimal]
    quantity: Optional[Decimal]
    authorization_certification_indicator: Optional[AuthorizationCertificationIndicator]
    inplan_network_indicator: Optional[InPlanNetworkIndicator]
    procedure_identifier: Optional[str]

    @root_validator
    def validate_quantity(cls, values):
        """
        Validates that both a quantity_qualifier and quantity are provided if one or the other is present

        :param values: The raw, unvalidated transaction data.
        """
        quantity_fields: Tuple = values.get("quantity_qualifier"), values.get(
            "quantity"
        )

        if any(quantity_fields) and not all(quantity_fields):
            raise ValueError("Quantity requires the quantity identifier and value.")

        return values


class EqSegment(X12Segment):
    """
    Eligibility Inquiry Segment
    Example:
        EQ*98^34^44^81^A0^A3**FAM~
    """

    segment_name: X12SegmentName = X12SegmentName.EQ
    service_type_code: Optional[List[str]]
    medical_procedure_id: Optional[List[str]] = Field(is_component=True)
    coverage_level_code: Optional[str] = Field(min_length=3, max_length=3)
    insurance_type_code: Optional[str] = Field(min_length=1, max_length=3)
    diagnosis_code_pointer: Optional[List[str]] = Field(is_component=True)

    @root_validator
    def validate_type_and_procedure_code(cls, values):
        """
        Validates that the EQ segment contains a service type code or a medical procedure id

        :param values: The raw, unvalidated transaction data.
        """
        reference_fields: Tuple = values.get("service_type_code"), values.get(
            "medical_procedure_id"
        )

        if not any(reference_fields):
            raise ValueError(
                "Service Type Code or Medical Procedure is required for EQ segment"
            )

        return values


class GeSegment(X12Segment):
    """
    Defines a functional header for the message and is an EDI control segment.
    Example:
        GE*1*1~
    """

    segment_name: X12SegmentName = X12SegmentName.GE
    number_of_transaction_sets_included: PositiveInt
    group_control_number: str = Field(min_length=1, max_length=9)


class GsSegment(X12Segment):
    """
    Defines a functional header for the message and is an EDI control segment.
    Example:
        GS*HS*000000005*54321*20131031*1147*1*X*005010X279A~
    """

    segment_name: X12SegmentName = X12SegmentName.GS
    functional_identifier_code: str = Field(min_length=2, max_length=2)
    application_sender_code: str = Field(min_length=2, max_length=15)
    application_receiver_code: str = Field(min_length=2, max_length=15)
    functional_group_creation_date: Union[str, datetime.date]
    functional_group_creation_time: Union[str, datetime.time]
    group_control_number: str = Field(min_length=1, max_length=9)
    responsible_agency_code: Literal["X"]
    version_identifier_code: str = Field(min_length=1, max_length=12)

    _validate_creation_date = field_validator("functional_group_creation_date")(
        parse_x12_date
    )
    _validate_creation_time = field_validator("functional_group_creation_time")(
        parse_x12_time
    )


class HiSegment(X12Segment):
    """
    Health Care Information/Diagnostic Codes
    Example:
         HI*BK:8901*BF:87200*BF:5559~
    """

    segment_name: X12SegmentName = X12SegmentName.HI
    health_care_code_1: List = Field(is_component=True)
    health_care_code_2: Optional[List] = Field(is_component=True)
    health_care_code_3: Optional[List] = Field(is_component=True)
    health_care_code_4: Optional[List] = Field(is_component=True)
    health_care_code_5: Optional[List] = Field(is_component=True)
    health_care_code_6: Optional[List] = Field(is_component=True)
    health_care_code_7: Optional[List] = Field(is_component=True)
    health_care_code_8: Optional[List] = Field(is_component=True)


class HlSegment(X12Segment):
    """
    Defines a hierarchical organization used to relate one grouping of segments to another
    Example:
        HL*3*2*22*1~
    """

    segment_name: X12SegmentName = X12SegmentName.HL
    hierarchical_id_number: str = Field(min_length=1, max_length=12)
    hierarchical_parent_id_number: str = Field(min_length=1, max_length=12)
    hierarchical_level_code: str = Field(min_length=1, max_length=2)
    hierarchical_child_code: str = Field(min_length=1, max_length=1, regex="^0|1$")


class HsdSegment(X12Segment):
    """
    Health Care Services Delivery
    Example:
        HSD*VS*12*WK*3*34*1~
    """

    class QuantityQualifier(str, Enum):
        """
        HSD01 code values
        """

        DAYS = "DY"
        UNITS = "FL"
        HOURS = "HS"
        MONTH = "MN"
        VISITS = "VS"

    class MeasurementCode(str, Enum):
        """
        HSD03 code values
        """

        DAYS = "DA"
        MONTHS = "MO"
        VISIT = "VS"
        WEEK = "WK"
        YEARS = "YR"

    class TimePeriodQualifier(str, Enum):
        """
        HD05 code values
        """

        HOURS = "6"
        DAY = "7"
        YEARS = "21"
        SERVICE_YEAR = "22"
        CALENDAR_YEAR = "23"
        YEAR_TO_DATE = "24"
        CONTRACT = "25"
        EPISODE = "26"
        VISIT = "27"
        OUTLIER = "28"
        REMAINING = "29"
        EXCEEDED = "30"
        NOT_EXCEEDED = "31"
        LIFETIME = "32"
        LIFETIME_RECURRING = "33"
        MONTH = "34"
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
        IMMEDIATELY = "M"
        AS_DIRECTED = "N"
        DAILY_MON_TO_FRI = "O"
        HALF_MON_HALF_THURS = "P"
        HALF_TUES_HALF_THURS = "Q"
        HALF_WED_HALF_FRIDAY = "R"
        ONCE_ANYTIME_MON_TO_FRI = "S"
        TUESDAY_TO_FRIDAY = "SG"
        MONDAY_TUESDAY_THURSDAY = "SL"
        MONDAY_TUESDAY_FRIDAY = "SP"
        WEDNESDAY_THURSDAY = "SX"
        MONDAY_WEDNESDAY_THURSDAY = "SY"
        TUESDAY_THURSDAY_FRIDAY = "SZ"
        HALF_TUESDAY_HALF_FRIDAY = "T"
        HALF_MONDAY_HALF_WEDNESDAY = "U"
        THIRD_MONDAY_THIRD_WEDNESDAY_THIRD_FRIDAY = "V"
        WHENEVER_NECESSARY = "W"
        HALF_BY_WEDNESDAY_BALANCE_BY_FRIDAY = "X"
        NONE_CANCEL_PREVIOUS_PATTERN = "Y"

    class DeliveryPatternTimeCode(str, Enum):
        """
        HSD08 code values
        """

        FIRST_SHIFT = "A"
        SECOND_SHIFT = "B"
        THIRD_SHIFT = "C"
        AM = "D"
        PM = "E"
        AS_DIRECTED = "F"
        ANY_SHIFT = "G"
        NONE_CANCEL_PREVIOUS_PATTERN = "Y"

    segment_name: X12SegmentName = X12SegmentName.HSD
    quantity_qualifier: Optional[QuantityQualifier]
    quantity: Optional[Decimal]
    measurement_code: Optional[MeasurementCode]
    sample_selection_modulus: Optional[Decimal]
    time_period_qualifier: Optional[TimePeriodQualifier]
    period_count: Optional[Decimal]
    delivery_frequency_code: Optional[DeliveryFrequencyCode]
    delivery_pattern_time_code: Optional[DeliveryPatternTimeCode]

    @root_validator
    def validate_quantity(cls, values):
        """
        Validates that quantity values are conveyed with a qualifier and value.

        :param values: The raw, unvalidated transaction data.
        """
        quantity_fields: Tuple = values.get("quantity_qualifier"), values.get(
            "quantity"
        )

        if not any(quantity_fields):
            raise ValueError("Quantity requires a qualifier and value")

        return values

    @root_validator
    def validate_periods(cls, values):
        """
        Validates that time periods are conveyed correctly
        """
        if values.get("period_count") and not values.get("time_period_qualifier"):
            raise ValueError("Period requires a qualifier and value")
        return values


class IeaSegment(X12Segment):
    """
    Defines the interchange footer and is an EDI control segment.
    Example:
        IEA*1*000000907~
    """

    segment_name: X12SegmentName = X12SegmentName.IEA
    number_of_included_functional_groups: PositiveInt
    interchange_control_number: str = Field(min_length=9, max_length=9)


class IiiSegment(X12Segment):
    """
    Additional Inquiry Information
    Example:
        III*ZZ*21~
    """

    class CodeListQualifierCode(str, Enum):
        """
        Code values for III01
        """

        NCCI_NATURE_OF_INJURY_CODE = "GR"
        NATURE_OF_INJURY_CODE = "NI"
        MUTUALLY_DEFINED = "ZZ"

    segment_name: X12SegmentName = X12SegmentName.III
    code_list_qualifier_code: Optional[CodeListQualifierCode]
    industry_code: Optional[str] = Field(min_length=1, max_length=30)
    code_category: Optional[Literal["44"]]
    injured_body_part_name: Optional[str] = Field(min_length=1, max_length=264)

    @root_validator
    def validate_industry_code(cls, values):
        """
        Validates that an industry code is conveyed with a qualifier and value, if sent at all.

        :param values: The validated model values.
        """
        industry_codes = values.get("code_list_qualifier_code"), values.get(
            "industry_code"
        )
        if any(industry_codes) and not all(industry_codes):
            raise ValueError("Industry codes require a qualifier and value")
        return values

    @root_validator
    def validate_nature_of_injury(cls, values):
        """
        Validates the nature of injury if present

        :param values: The validated model values
        """
        if values.get("code_category") and not values.get("injured_body_part_name"):
            raise ValueError(
                "Nature of injury requires a category and value/description"
            )
        return values


class InsSegment(X12Segment):
    """
    Insured benefit.
    Example:
        INS*Y*18*021*28*A***FT~
    """

    class ResponseCode(str, Enum):
        """
        INS01 code values
        """

        NO = "N"
        YES = "Y"

    segment_name: X12SegmentName = X12SegmentName.INS
    member_indicator: ResponseCode
    individual_relationship_code: str = Field(min_length=2, max_length=2)
    maintenance_type_code: str = Field(min_length=3, max_length=3)
    maintenance_reason_code: Optional[str] = Field(min_length=2, max_length=3)
    benefit_status_code: str = Field(min_length=1, max_length=1)
    medicare_status_code: Optional[List[str]] = Field(is_component=True)
    cobra_qualifying_event_code: Optional[str] = Field(min_length=1, max_length=2)
    employment_status_code: Optional[str] = Field(min_length=2, max_length=2)
    student_status_code: Optional[str] = Field(min_length=1, max_length=1)
    handicap_indicator: Optional[ResponseCode]
    date_time_period_format_qualifier: Optional[str] = Field(min_length=2, max_length=3)
    member_death_date: Optional[Union[str, datetime.date]]
    confidentiality_code: Optional[str] = Field(min_length=1, max_length=1)
    city_name: Optional[str] = Field(min_length=2, max_length=30)
    state_province_code: Optional[str] = Field(min_length=2, max_length=2)
    country_code: Optional[str] = Field(min_length=2, max_length=3)
    birth_sequence_number: Optional[int]

    _validate_death_date = field_validator("member_death_date")(validate_date_field)

    @root_validator
    def validate_member_death_datefields(cls, values):
        """
        Validates that both a date_time_period_format_qualifier and member_death_date are provided if one or the other is present

        :param values: The raw, unvalidated transaction data.
        """
        date_fields: Tuple = values.get(
            "date_time_period_format_qualifier"
        ), values.get("member_death_date")

        if any(date_fields) and not all(date_fields):
            raise ValueError(
                "If member death date is reported both date time format qualifier and member_death_date are required."
            )

        return values


class IsaSegment(X12Segment):
    """
    Defines the interchange header and is an EDI control segment.
    The ISA Segment is a fixed length segment (106 characters)
    Example:
        ISA*03*9876543210*01*9876543210*30*000000005      *30*12345          *131031*1147*^*00501*000000907*1*T*:~
    """

    segment_name: X12SegmentName = X12SegmentName.ISA
    authorization_information_qualifier: str = Field(min_length=2, max_length=2)
    authorization_information: str = Field(min_length=10, max_length=10)
    security_information_qualifier: str = Field(min_length=2, max_length=2)
    security_information: str = Field(min_length=10, max_length=10)
    interchange_sender_qualifier: str = Field(min_length=2, max_length=2)
    interchange_sender_id: str = Field(min_length=15, max_length=15)
    interchange_receiver_qualifier: str = Field(min_length=2, max_length=2)
    interchange_receiver_id: str = Field(min_length=15, max_length=15)
    interchange_date: Union[str, datetime.date]
    interchange_time: Union[str, datetime.time]
    repetition_separator: str = Field(min_length=1, max_length=1)
    interchange_control_version_number: str = Field(min_length=5, max_length=5)
    interchange_control_number: str = Field(min_length=9, max_length=9)
    acknowledgment_requested: str = Field(min_length=1, max_length=1)
    interchange_usage_indicator: str = Field(min_length=1, max_length=1)
    component_element_separator: str = Field(min_length=1, max_length=1)

    _validate_interchange_date = field_validator("interchange_date")(
        parse_interchange_date
    )
    _validate_interchange_time = field_validator("interchange_time")(parse_x12_time)

    def x12(self) -> str:
        """
        Overriden to support formatting the interchange date as yymmdd ( %y%m%d )
        """
        x12_string: str = super().x12()
        segment_fields = x12_string.split(self.delimiters.element_separator)

        interchange_date = datetime.datetime.strptime(
            segment_fields[9], "%Y%m%d"
        ).date()
        segment_fields[9] = interchange_date.strftime("%y%m%d")

        return self.delimiters.element_separator.join(segment_fields)


class LeSegment(X12Segment):
    """
    Loop trailer segment.
    Used to "close" a loop grouping opened by a LS segment.
    Example:
        LE*2120~
    """

    segment_name: X12SegmentName = X12SegmentName.LE
    loop_id_code: str


class LsSegment(X12Segment):
    """
    Loop Header Segment.
    The LS segment is used to disambiguate loops which start with the same segment.
    Example:
        LS*2120~
    """

    segment_name: X12SegmentName = X12SegmentName.LS
    loop_id_code: str


class MpiSegment(X12Segment):
    """
    Military Personnel Information
    """

    class InformationStatusCode(str, Enum):
        """
        Code values for MPI01
        """

        PARTIAL = "P"
        CURRENT = "C"
        LATEST = "L"
        OLDEST = "O"
        PRIOR = "P"
        SECOND_MOST_CURRENT = "S"
        THIRD_MOST_CURRENT = "T"

    class EmploymentStatusCode(str, Enum):
        """
        Code values for MPI02
        """

        ACTIVE_RESERVE = "AE"
        ACTIVE_MILITARY_OVERSEAS = "AO"
        ACADEMY_STUDENT = "AS"
        PRESIDENTIAL_APPOINTEE = "AT"
        ACTIVE_MILITARY_USA = "AU"
        CONTRACTOR = "CC"
        DISHONORABLY_DISCHARGED = "DD"
        HONORABLY_DISCHARGED = "HD"
        INACTIVE_RESERVES = "IR"
        LEAVE_OF_ABSENCE_MILITARY = "LX"
        PLAN_TO_ENSLIST = "PE"
        RECOMISSIONED = "RE"
        RETIRED_MILITARY_OVERSEAS = "RM"
        RETIRED_WITHOUT_RECALL = "RR"
        RETIRED_MILITARY_USA = "RU"

    class GovernmentServicesAffiliationCode(str, Enum):
        """
        Code values for MPI03
        """

        AIR_FORCE = "A"
        AIR_FORCE_RESERVE = "B"
        ARMY = "C"
        ARMY_RESERVES = "D"
        COAST_GUARD = "E"
        MARINE_CORPS = "F"
        MARINE_CORPS_RESERVE = "G"
        NATIONAL_GUARD = "H"
        NAVY = "I"
        NAVY_RESERVES = "J"
        OTHER = "K"
        PEACE_CORP = "L"
        REGULAR_ARMED_FORCES = "M"
        RESERVES = "N"
        US_PUBLIC_HEALTH_SERVICE = "O"
        FOREIGN_MILITARY = "Q"
        AMERICAN_RED_CROSS = "R"
        DEPARTMENT_OF_DEFENSE = "S"
        UNITED_SERVICES_ORGANIZATION = "U"
        MILITARY_SEALIFT_COMMAND = "W"

    class MilitaryServiceRankCode(str, Enum):
        """
        Code values for MPI05
        """

        ADMIRAL = "A1"
        AIRMAN = "A2"
        AIRMAN_FIRST_CLASS = "A3"
        BASIC_AIRMAN = "B1"
        BRIGADIER_GENERAL = "B2"
        CAPTAIN = "C1"
        CHIEF_MASTER_SERGEANT = "C2"
        CHIEF_PETTY_OFFICER = "C3"
        CHIEF_WARRANT = "C4"
        COLONEL = "C5"
        COMMANDER = "C6"
        COMMODORE = "C7"
        CORPORAL = "C8"
        CORPORAL_SPECIALIST_4 = "C9"
        ENSIGN = "E1"
        FIRST_LIEUTENANT = "F1"
        FIRST_SERGEANT = "F2"
        FIRST_SERGEANT_MASTER_SERGEANT = "F3"
        FLEET_ADMIRAL = "F4"
        GENERAL = "G1"
        GUNNERY_SERGEANT = "G4"
        LANCE_CORPORAL = "L1"
        LIEUTENANT = "L2"
        LIEUTENANT_COLONEL = "L3"
        LIEUTENANT_COMMANDER = "L4"
        LIEUTENANT_GENERAL = "L5"
        LIEUTENANT_JUNIOR_GRADE = "L6"
        MAJOR = "M1"
        MAJOR_GENERAL = "M2"
        MASTER_CHIEF_PETTY_OFFICER = "M3"
        MASTER_GUNNERY_SERGEANT_MAJOR = "M4"
        MASTER_SERGEANT = "M5"
        MASTER_SERGEANT_SPECIALIST_8 = "M6"
        PETTY_OFFICER_FIRST_CLASS = "P1"
        PETTY_OFFICER_SECOND_CLASS = "P2"
        PETTY_OFFICER_THIRD_CLASS = "P3"
        PRIVATE = "P4"
        PRIVATE_FIRST_CLASS = "P5"
        REAR_ADMIRAL = "R1"
        RECRUIT = "R2"
        SEAMAN = "S1"
        SEAMAN_APPRENTICE = "S2"
        SEAMAN_RECRUIT = "S3"
        SECOND_LIEUTENANT = "S4"
        SENIOR_CHIEF_PETTY_OFFICER = "S5"
        SENIOR_MASTER_SERGEANT = "S6"
        SERGEANT = "S7"
        SERGEANT_FIRST_CLASS_SPECIALIST_7 = "S8"
        SERGEANT_MAJOR_SPECIALIST_9 = "S9"
        SERGEANT_SPECIALIST_5 = "SA"
        STAFF_SERGEANT = "SB"
        STAFF_SERGEANT_SPECIALIST_6 = "SC"
        TECHNICAL_SERGEANT = "T1"
        VICE_ADMIRAL = "V1"
        WARRANT_OFFICER = "W1"

    class DateTimePeriodFormatQualifier(str, Enum):
        """
        Code values for MPI06
        """

        DATE = "D8"
        DATE_RANGE = "RD8"

    segment_name: X12SegmentName = X12SegmentName.MPI
    information_status_code: InformationStatusCode
    employment_status_code: EmploymentStatusCode
    government_services_affiliation_code: GovernmentServicesAffiliationCode
    description: Optional[str]
    military_service_rank_code: Optional[MilitaryServiceRankCode]
    date_time_period_format_qualifier: Optional[DateTimePeriodFormatQualifier]
    date_time_period: Optional[str]

    @root_validator
    def validate_date_fields(cls, values):
        """
        Validates that both a date_time_format_qualifier and date_time_period are provided if one or the other is present

        :param values: The raw, unvalidated transaction data.
        """
        date_fields: Tuple = values.get("date_time_format_qualifier"), values.get(
            "date_time_period"
        )

        if any(date_fields) and not all(date_fields):
            raise ValueError(
                "If either date_time_period_format_qualifier or date_time_period are provided, both are required"
            )

        return values


class MsgSegment(X12Segment):
    """
    Message segment - for free form text.
    """

    segment_name: X12SegmentName = X12SegmentName.MSG
    free_form_text: str


class N3Segment(X12Segment):
    """
    Party Location (Address)
    Example:
        N3*201 PARK AVENUE*SUITE 300~
    """

    segment_name: X12SegmentName = X12SegmentName.N3
    address_information_1: str = Field(min_length=1, max_length=55)
    address_information_2: Optional[str] = Field(min_length=1, max_length=55)


class N4Segment(X12Segment):
    """
    Geographic Location (Address)
    Example:
        N4*KANSAS CITY*MO*64108~
    """

    segment_name: X12SegmentName = X12SegmentName.N4
    city_name: str = Field(min_length=2, max_length=30)
    state_province_code: Optional[str] = Field(min_length=2, max_length=2)
    postal_code: Optional[str] = Field(min_length=3, max_length=15)
    country_code: Optional[str] = Field(min_length=2, max_length=3)
    location_qualifier: Optional[str] = Field(min_length=1, max_length=2)
    location_identifier: Optional[str] = Field(min_length=1, max_length=30)
    country_subdivision_code: Optional[str] = Field(min_length=1, max_length=3)

    @root_validator
    def validate_state_codes(cls, values):
        """
        Validates that a N4 segment does not contain both a state_province_code and country_subdivision_code

        :param values: The raw, unvalidated transaction data.
        """
        state_fields: Tuple = values.get("state_province_code"), values.get(
            "country_subdivision_code"
        )

        if all(state_fields):
            raise ValueError(
                "only one of state_province_code or country_subdivision_code is allowed"
            )

        return values


class Nm1Segment(X12Segment):
    """
    Entity Name and Identification Number
    Example:
        NM1*PR*2*PAYER C*****PI*12345~
    """

    class EntityQualifierCode(str, Enum):
        """
        NM1.02 Entity Qualifier Code to specify the entity type
        """

        PERSON = "1"
        NON_PERSON = "2"

    segment_name: X12SegmentName = X12SegmentName.NM1
    entity_identifier_code: str = Field(min_length=2, max_length=3)
    entity_type_qualifier: EntityQualifierCode
    name_last_or_organization_name: str = Field(min_length=1, max_length=60)
    name_first: Optional[str] = Field(min_length=0, max_length=35)
    name_middle: Optional[str] = Field(min_length=0, max_length=25)
    name_prefix: Optional[str]
    name_suffix: Optional[str] = Field(min_length=0, max_length=10)
    identification_code_qualifier: Optional[str] = Field(min_length=1, max_length=2)
    identification_code: Optional[str] = Field(min_length=2, max_length=80)
    # NM110 - NM112 are not used

    @root_validator
    def validate_identification_codes(cls, values):
        """
        Validates that both an identification code and qualifier are provided if one or the other is present

        :param values: The raw, unvalidated transaction data.
        """
        id_fields: Tuple = values.get("identification_code_qualifier"), values.get(
            "identification_code"
        )

        if any(id_fields) and not all(id_fields):
            raise ValueError(
                "Identification code usage requires the code qualifier and code value"
            )

        return values

    @validator("name_first", "name_middle", "name_prefix", "name_suffix")
    def validate_organization_name_fields(cls, field_value, values):
        """
        Validates that person name fields are not used within an organizational record context.

        :param field_value: The person name field (first, middle, prefix, suffix) values
        :param values: The previously validated field names and values
        """
        entity_type = values["entity_type_qualifier"]

        if cls.EntityQualifierCode.NON_PERSON.value == entity_type:
            if field_value:
                raise ValueError(
                    "Invalid field usage for Organization/Non-Person Entity"
                )
        return field_value


class PerSegment(X12Segment):
    """
    EDI Contact Information
    Example:
        PER*IC*JOHN SMITH*TE*5551114444*EX*123~
    """

    class ContactFunctionCode(str, Enum):
        """
        Code value for PER01
        """

        INFORMATION_CONTACT = "IC"

    segment_name: X12SegmentName = X12SegmentName.PER
    contact_function_code: ContactFunctionCode
    name: Optional[str]
    communication_number_qualifier_1: str
    communication_number_1: str
    communication_number_qualifier_2: Optional[str]
    communication_number_2: Optional[str]
    communication_number_qualifier_3: Optional[str]
    communication_number_3: Optional[str]

    @root_validator
    def validate_communication(cls, values):
        """
        Validates that both a communication qualifier and number are provided if one or the other is present

        :param values: The raw, unvalidated transaction data.
        """
        communication_fields: Tuple = values.get(
            "communication_number_qualifier_2"
        ), values.get("communication_number_2")

        if any(communication_fields) and not all(communication_fields):
            raise ValueError("communication fields require a qualifier and number")

        communication_fields = values.get(
            "communication_number_qualifier_3"
        ), values.get("communication_number_3")

        if any(communication_fields) and not all(communication_fields):
            raise ValueError("communication fields require a qualifier and number")

        return values


class PrvSegment(X12Segment):
    """
    Provider Information
    Example:
        PRV*RF*PXC*207Q00000X~
    """

    segment_name: X12SegmentName = X12SegmentName.PRV
    provider_code: str = Field(min_length=1, max_length=3)
    reference_identification_qualifier: Optional[str] = Field(
        min_length=2, max_length=3
    )
    reference_identification: Optional[str] = Field(min_length=1, max_length=50)

    @root_validator
    def validate_reference_id(cls, values):
        """
        Validates that both an identification value and qualifier are provided if one or the other is present

        :param values: The raw, unvalidated transaction data.
        """
        reference_fields: Tuple = values.get(
            "reference_identification_qualifier"
        ), values.get("reference_identification")

        if any(reference_fields) and not all(reference_fields):
            raise ValueError(
                "only one of reference_identification_qualifier or reference_identification is allowed"
            )

        return values


class RefSegment(X12Segment):
    """
    Reference Identification
    Example:
        REF*EO*477563928~
    """

    segment_name: X12SegmentName = X12SegmentName.REF
    reference_identification_qualifier: str = Field(min_length=2, max_length=3)
    reference_identification: str = Field(min_length=1, max_length=50)
    description: Optional[str] = Field(min_length=1, max_length=80)


class SeSegment(X12Segment):
    """
    Transaction Set Footer
    Example:
        SE*17*0001~
    """

    segment_name: X12SegmentName = X12SegmentName.SE
    transaction_segment_count: PositiveInt
    transaction_set_control_number: str = Field(min_length=4, max_length=9)


class StSegment(X12Segment):
    """
    Transaction Set Header.
    Example:
        ST*270*0001*005010X279A1~
    """

    segment_name: X12SegmentName = X12SegmentName.ST
    transaction_set_identifier_code: str = Field(min_length=3, max_length=3)
    transaction_set_control_number: str = Field(min_length=4, max_length=9)
    implementation_convention_reference: str = Field(min_length=1, max_length=35)


class TrnSegment(X12Segment):
    """
    Trace Number Segment
    Example:
        TRN*1*98175-012547*8877281234*RADIOLOGY~
    """

    segment_name: X12SegmentName = X12SegmentName.TRN
    trace_type_code: str = Field(min_length=1, max_length=2)
    reference_identification_1: str = Field(min_length=1, max_length=50)
    originating_company_identifier: str = Field(min_length=10, max_length=10)
    reference_identification_2: Optional[str] = Field(min_length=1, max_length=50)


# load segment classes into a lookup table indexed by segment name
SEGMENT_LOOKUP: Dict = {}

cached_attrs = [v for v in globals().values()]

for a in cached_attrs:
    if hasattr(a, "x12") and a.__name__ != "X12Segment":
        # clean up the string representation to limit it to the 2 - 3 character segment name
        # use pydantic metadata to grab the default value assigned to segment_name
        # this value is X12SegmentName[SegmentCode]
        segment_key: str = str(a.__fields__["segment_name"].default).replace(
            "X12SegmentName.", ""
        )
        SEGMENT_LOOKUP[segment_key] = a
