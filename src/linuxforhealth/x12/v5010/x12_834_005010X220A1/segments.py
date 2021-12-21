"""
segments.py

Specialized segment models for the Enrollment 834 005010X220A1 transaction.
"""
from typing import Literal, Optional
from enum import Enum
from pydantic import Field

from linuxforhealth.x12.v5010.segments import (
    StSegment,
    RefSegment,
    DtpSegment,
    QtySegment,
    N1Segment,
    InsSegment,
    Nm1Segment,
    PerSegment,
    DmgSegment,
    AmtSegment,
    PlaSegment,
    LsSegment,
    LeSegment,
)


class HeaderStSegment(StSegment):
    """
    Customized ST segment for 834 transaction header
    """

    transaction_set_identifier_code: Literal["834"]
    implementation_convention_reference: Literal["005010X220A1"]


class HeaderRefSegment(RefSegment):
    """
    Transaction Set Policy Number
    """

    reference_identification_qualifier: Literal["38"]


class HeaderDtpSegment(DtpSegment):
    """
    File Effective Date
    """

    class DateTimeQualifier(str, Enum):
        """
        DTP01 code values
        """

        EFFECTIVE = "007"
        REPORT_START = "090"
        REPORT_END = "091"
        MAINTENANCE_EFFECTIVE = "303"
        ENROLLMENT = "382"
        PAYMENT_COMMENCEMENT = "388"

    date_time_qualifier: DateTimeQualifier
    date_time_period_format_qualifier: Literal["D8"]


class HeaderQtySegment(QtySegment):
    """
    Transaction Set Control Totals
    """

    class QuantityQualifier(str, Enum):
        """
        Code values for QTY01
        """

        DEPENDENT_TOTAL = "DT"
        EMPLOYEE_TOTAL = "ET"
        TOTAL = "TO"

    quantity_qualifier: QuantityQualifier


class Loop1000AN1Segment(N1Segment):
    """
    Loop 1000A Sponsor Name
    """

    class IdentificationCodeQualifier(str, Enum):
        """
        Code values for N103
        """

        EMPLOYER_IDENTIFICATION_NUMBER = "24"
        ORGANIZATION_ASSIGNED_CODE = "94"
        FEDERAL_TAXPAYER_IDENTIFICATION_NUMBER = "FI"

    entity_identifier_code: Literal["P5"]
    name: Optional[str] = Field(min_length=1, max_length=60)
    identification_code_qualifier: IdentificationCodeQualifier


class Loop1000BN1Segment(N1Segment):
    """
    Loop 1000B Payer Name
    """

    class IdentificationCodeQualifier(str, Enum):
        """
        Code values for N103
        """

        ORGANIZATION_ASSIGNED_CODE = "94"
        FEDERAL_TAXPAYER_IDENTIFICATION_NUMBER = "FI"
        CMS_PLAN_ID = "XV"

    entity_identifier_code: Literal["IN"]
    name: Optional[str] = Field(min_length=1, max_length=60)
    identification_code_qualifier: IdentificationCodeQualifier


class Loop1000CN1Segment(N1Segment):
    """
    Loop 1000C TPA/Broker Name
    """

    class EntityIdentifierCode(str, Enum):
        """
        Code values for N101
        """

        BROKER_SALES_OFFICE = "BO"
        THIRD_PARTY_ADMINISTRATOR = "TV"

    class IdentificationCodeQualifier(str, Enum):
        """
        Code values for N103
        """

        ORGANIZATION_ASSIGNED_CODE = "94"
        FEDERAL_TAXPAYER_IDENTIFICATION_NUMBER = "FI"
        CMS_PLAN_ID = "XV"

    entity_identifier_code: EntityIdentifierCode
    identification_code_qualifier: IdentificationCodeQualifier


class Loop2000InsSegment(InsSegment):
    """
    Member level detail insurance information
    """

    class IndividualRelationshipCode(str, Enum):
        """
        Code values for INS02
        """

        SPOUSE = "01"
        FATHER_OR_MOTHER = "03"
        GRANDFATHER_OR_GRANDMOTHER = "04"
        GRANDSON_OR_GRANDDAUGHTER = "05"
        UNCLE_OR_AUNT = "06"
        NEPHEW = "07"
        COUSIN = "08"
        ADOPTED_CHILD = "09"
        FOSTER_CHILD = "10"
        SON_OR_DAUGHTER_IN_LAW = "11"
        BROTHER_OR_SISTER_IN_LAW = "12"
        MOTHER_OR_FATHER_IN_LAW = "13"
        BROTHER_OR_SISTER = "14"
        WARD = "15"
        STEPPARENT = "16"
        STEPSON_OR_STEPDAUGHTER = "17"
        SELF = "18"
        CHILD = "19"
        SPONSORED_DEPENDENT = "23"
        DEPENDENT_OF_MINOR_DEPENDENT = "24"
        EX_SPOUSE = "25"
        GUARDIAN = "26"
        COURT_APPOINTED_GUARDIAN = "31"
        COLLATERAL_DEPENDENT = "38"
        LIFE_PARTNER = "53"
        ANNUITANT = "60"
        TRUSTEE = "D2"
        OTHER_RELATIONSHIP = "G8"
        OTHER_RELATIVE = "G9"

    class MaintenanceTypeCode(str, Enum):
        """
        Code values for INS03
        """

        CHANGE = "001"
        ADDITION = "021"
        CANCELLATION_OR_TERMINATION = "024"
        REINSTATEMENT = "025"
        AUDIT_OR_COMPARE = "030"

    class MaintenanceReasonCode(str, Enum):
        """
        Code values for INS04
        """

        DIVORCE = "01"
        BIRTH = "02"
        DEATH = "03"
        RETIREMENT = "04"
        ADOPTION = "05"
        STRIKE = "06"
        TERMINATION_OF_BENEFITS = "07"
        TERMINATION_OF_EMPLOYMENT = "08"
        COBRA = "09"
        COBRA_PREMIUM_PAID = "10"
        SURVIVING_SPOUSE = "11"
        VOLUNTARY_WITHDRAWL = "14"
        PRIMARY_CARE_PROVIDER_CHANGE = "15"
        QUIT = "16"
        FIRED = "17"
        SUSPENDED = "18"
        ACTIVE = "20"
        DISABILITY = "21"
        PLAN_CHANGE = "22"
        CHANGE_IN_IDENTIFYING_ELEMENTS = "25"
        DECLINED_COVERAGE = "26"
        PRE_ENROLLMENT = "27"
        INITIAL_ENROLLMENT = "28"
        BENEFIT_SELECTION = "29"
        LEGAL_SEPARATION = "31"
        MARRIAGE = "32"
        PERSONNEL_DATA = "33"
        LEAVE_OF_ABSENCE_WITH_BENEFITS = "37"
        LEAVE_OF_ABSENCE_WITHOUT_BENEFITS = "38"
        LAY_OFF_WITH_BENEFITS = "39"
        LAY_OFF_WITHOUT_BENEFITS = "40"
        RE_ENROLLMENT = "41"
        CHANGE_OF_LOCATION = "43"
        NON_PAYMENT = "59"
        DISSATISFACTION_WITH_OFFICE_STAFF = "AA"
        DISSATISFACTION_WITH_MEDICAL_CARE_SERVICES = "AB"
        INCONVENIENT_OFFICE_LOCATION = "AC"
        DISSATISFACTION_WITH_OFFICE_HOURS = "AD"
        UNABLE_TO_SCHEDULE_APPOINTMENTS_IN_TIMELY_MANNER = "AE"
        DISSATISFACTION_WITH_PHYSICIANS_REFERRAL_POLICY = "AF"
        LESS_RESPECT_AND_ATTENTION_GIVEN_THAN_TO_OTHER_PATIENTS = "AG"
        PATIENT_MOVED_NEW_LOCATION = "AH"
        NO_REASON_GIVEN = "AI"
        APPOINTMENT_TIMES_NOT_MET_IN_TIMELY_MANNER = "AJ"
        ALGORITHM_ASSIGNED_BENEFIT_SELECTION = "AL"
        MEMBER_BENEFIT_SELECTION = "EC"
        NOTIFICATION_ONLY = "XN"
        TRANSFER = "XT"

    class BenefitStatusCode(str, Enum):
        """
        Code values for INS05
        """

        ACTIVE = "A"
        COBRA = "C"
        SURVIVING_INSURED = "S"
        TAX_EQUITY_FISCAL_RESPONSIBILITY = "T"

    class CobraQualifying(str, Enum):
        """
        Code values for INS07
        """

        TERMINATION_OF_EMPLOYMENT = "1"
        REDUCTION_OF_WORK_HOURS = "2"
        MEDICARE = "3"
        DEATH = "4"
        DIVORCE = "5"
        SEPARATION = "6"
        INELIGIBLE_CHILD = "7"
        BANKRUPTCY_RETIRE_FORMER_EMPLOYER = "8"
        LAYOFF = "9"
        LEAVE_OF_ABSENCE = "10"
        MUTUALLY_DEFINED = "ZZ"

    class EmploymentStatusCode(str, Enum):
        """
        Code values for INS08
        """

        ACTIVE_MILITARY_OVERSEAS = "AO"
        ACTIVE_MILITARY_USA = "AU"
        FULL_TIME = "FT"
        LEAVE_OF_ABSENCE = "L1"
        PART_TIME = "PT"
        RETIRED = "RT"
        TERMINATED = "TE"

    class StudentStatusCode(str, Enum):
        """
        Code values for INS09
        """

        FULL_TIME = "F"
        NOT_A_STUDENT = "N"
        PART_TIME = "P"

    class ConfidentiallyCode(str, Enum):
        """
        Code values for INS13
        """

        RESTRICTED_ACCESS = "R"
        UNRESTRICTED_ACCESS = "U"

    individual_relationship_code: IndividualRelationshipCode
    maintenance_type_code: MaintenanceTypeCode
    maintenance_reason_code: Optional[MaintenanceReasonCode]
    benefit_status_code: BenefitStatusCode
    cobra_qualifying_event_code: Optional[CobraQualifying]
    employment_status_code: Optional[EmploymentStatusCode]
    student_status_code: Optional[StudentStatusCode]
    handicap_indicator: Optional[InsSegment.ResponseCode]
    confidentiality_code: Optional[ConfidentiallyCode]


class Loop2000RefSegment(RefSegment):
    """ "
    Member level detail reference identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        SUBSCRIBER_NUMBER = "0F"
        GROUP_OR_POLICY_NUMBER = "1L"
        CLIENT_REPORTING_CATEGORY = "17"
        CLIENT_NUMBER = "23"
        CASE_NUMBER = "3H"
        PERSONAL_IDENTIFICATION_NUMBER = "4A"
        CROSS_REFERENCE_NUMBER = "60"
        PERSONAL_ID_NUMBER = "ABB"
        PDP_PHARMACY_NUMBER = "D3"
        DEPARTMENT_AGENCY_NUMBER = "DX"
        HEALTH_INSURANCE_CLAIM_NUMBER = "HIC"
        POSITION_CODE = "P5"
        PRIOR_IDENTIFIER_NUMBER = "Q4"
        UNIT_NUMBER = "QQ"
        MUTUALLY_DEFINED = "ZZ"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2000DtpSegment(DtpSegment):
    """ "
    Member level detail dates
    """

    class DateTimeQualifier(str, Enum):
        """
        Code values for DTP01
        """

        RECEIVED = "050"
        RETIREMENT = "286"
        INITIAL_DISABILITY_PERIOD_RETURN_TO_WORK = "296"
        INITIAL_DISABILITY_PERIOD_LAST_DAY_WORKED = "297"
        ENROLLMENT_SIGNATURE_DATE = "300"
        COBRA_QUALIFYING_EVENT = "301"
        MAINTENANCE_EFFECTIVE = "303"
        EMPLOYMENT_BEGIN = "336"
        EMPLOYMENT_END = "337"
        MEDICARE_BEGIN = "338"
        MEDICARE_END = "339"
        COBRA_BEGIN = "340"
        COBRA_END = "341"
        EDUCATION_BEGIN = "350"
        EDUCATION_END = "351"
        ELIGIBILITY_BEGIN = "356"
        ELIGIBILITY_END = "357"
        ADJUSTED_HIRE = "383"
        CREDITED_SERVICE_BEGIN = "385"
        CREDITED_SERVICE_END = "386"
        PLAN_PARTICIPATION_SUSPENSION = "393"
        REHIRE = "394"
        MEDICAID_BEGIN = "473"
        MEDICAID_END = "474"

    date_time_qualifier: DateTimeQualifier


class Loop2100ANm1Segment(Nm1Segment):
    """
    Member Name
    """

    class EntityIdentifierCode(str, Enum):
        """
        Code values for NM101
        """

        CORRECTED_INUSRED = "74"
        INSURED_OR_SUBSCRIBER = "IL"

    class IdentificationCodeQualifier(str, Enum):
        """
        Code values for NM108
        """

        SOCIAL_SECURITY_NUMBER = "34"
        MUTUALLY_DEFINED = "ZZ"

    entity_identifier_code: EntityIdentifierCode
    identification_code_qualifier: Optional[IdentificationCodeQualifier]


class BenefitEnrollmentPerSegment(PerSegment):
    """
    Member communication numbers
    """

    class CommunicationNumberQualifier(str, Enum):
        """
        Code values for PER03
        """

        ALTERNATE_TELEPHONE = "AP"
        BEEPER_NUMBER = "BN"
        CELLULAR_PHONE = "CP"
        ELECTRONIC_MAIL = "EM"
        TELEPHONE_EXTENSION = "EX"
        FACSIMILE = "FX"
        HOME_PHONE_NUMBER = "HP"
        TELEPHONE = "TE"
        WORK_PHONE_NUMBER = "WP"

    contact_function_code: Literal["IP"]
    name: Optional[str] = Field(min_length=1, max_length=60)
    communication_number_qualifier_1: CommunicationNumberQualifier
    communication_number_qualifier_2: Optional[CommunicationNumberQualifier]
    communication_number_qualifier_3: Optional[CommunicationNumberQualifier]


class Loop2100ADmgSegment(DmgSegment):
    """
    Member demographics
    """

    class MaritalStatusCode(str, Enum):
        """
        Code values for DMG04
        """

        REGISTERED_DOMESTIC_PARTNER = "B"
        DIVORCED = "D"
        SINGLE = "I"
        MARRIED = "M"
        UNREPORTED = "R"
        SEPARATED = "S"
        UNMARRIED = "U"
        WIDOWED = "W"
        LEGALLY_SEPARATED = "X"

    class CitizenshipStatusCode(str, Enum):
        """
        Code values for DMG06
        """

        US_CITIZEN = "1"
        NON_RESIDENT_ALIEN = "2"
        RESIDENT_ALIEN = "3"
        ILLEGAL_ALIEN = "4"
        ALIEN = "5"
        US_CITIZEN_NON_RESIDENT = "6"
        US_CITIZEN_RESIDENT = "7"

    marital_status_code: Optional[MaritalStatusCode]
    citizenship_status_code: Optional[CitizenshipStatusCode]
    code_list_qualifier_code: Optional[Literal["REC"]]


class Loop2100AAmtSegment(AmtSegment):
    """
    Member Policy Amounts
    """

    class AmountQualifierCode(str, Enum):
        """
        Code values for AMT01
        """

        COINSURANCE_ACTUAL = "B9"
        COPAYMENT_AMOUNT = "C1"
        DEDUCTIBLE_AMOUNT = "D2"
        EXPECTED_EXPENDITURE_AMOUNT = "EBA"
        OTHER_UNLISTED_AMOUNT = "FK"
        PREMIMUM_AMOUNT = "P3"
        SPEND_DOWN = "R"

    amount_qualifier_code: AmountQualifierCode


class Loop2100BNm1Segment(Nm1Segment):
    """
    Incorrect member name segment
    """

    class IdentificationCodeQualifier(str, Enum):
        """
        Code values for NM108
        """

        SOCIAL_SECURITY_NUMBER = "34"
        MUTUALLY_DEFINED = "ZZ"

    entity_identifier_code: Literal["70"]
    entity_type_qualifier: Literal["1"]
    identification_code_qualifier: Optional[IdentificationCodeQualifier]


class Loop2100BDmgSegment(DmgSegment):
    """
    Incorrect Member demographics
    """

    class MaritalStatusCode(str, Enum):
        """
        Code values for DMG04
        """

        REGISTERED_DOMESTIC_PARTNER = "B"
        DIVORCED = "D"
        SINGLE = "I"
        MARRIED = "M"
        UNREPORTED = "R"
        SEPARATED = "S"
        UNMARRIED = "U"
        WIDOWED = "W"
        LEGALLY_SEPARATED = "X"

    class CitizenshipStatusCode(str, Enum):
        """
        Code values for DMG06
        """

        US_CITIZEN = "1"
        NON_RESIDENT_ALIEN = "2"
        RESIDENT_ALIEN = "3"
        ILLEGAL_ALIEN = "4"
        ALIEN = "5"
        US_CITIZEN_NON_RESIDENT = "6"
        US_CITIZEN_RESIDENT = "7"

    marital_status_code: Optional[MaritalStatusCode]
    citizenship_status_code: Optional[CitizenshipStatusCode]
    code_list_qualifier_code: Optional[Literal["REC"]]


class Loop2100CNm1Segment(Nm1Segment):
    """
    Member mailing address
    """

    entity_identifier_code: Literal["31"]
    entity_type_qualifier: Literal["1"]
    identification_code_qualifier: Optional[str]
    identification_code: Optional[str]


class Loop2100DNm1Segment(Nm1Segment):
    """
    Member employer
    """

    class IdentificationCodeQualifier(str, Enum):
        """
        Code values for NM108
        """

        SOCIAL_SECURITY_NUMBER = "34"
        MUTUALLY_DEFINED = "ZZ"

    entity_identifier_code: Literal["36"]
    identification_code_qualifier: Optional[IdentificationCodeQualifier]


class Loop2100ENm1Segment(Nm1Segment):
    """
    Member School
    """

    entity_identifier_code: Literal["M8"]
    name_last_or_organization_name: str = Field(min_length=1, max_length=80)
    identification_code_qualifier: Optional[str]
    identification_code: Optional[str]


class Loop2100FNm1Segment(Nm1Segment):
    """
    Member Custodial Parent
    """

    class IdentificationCodeQualifier(str, Enum):
        """
        Code values for NM108
        """

        SOCIAL_SECURITY_NUMBER = "34"
        MUTUALLY_DEFINED = "ZZ"

    entity_identifier_code: Literal["S3"]
    entity_type_qualifier: Literal["1"]
    name_last_or_organization_name: str = Field(min_length=1, max_length=60)
    name_first: Optional[str] = Field(min_length=1, max_length=35)
    identification_code_qualifier: Optional[IdentificationCodeQualifier]
    identification_code: Optional[str] = Field(min_length=2, max_length=80)


class Loop2100GNm1Segment(Nm1Segment):
    """
    Member Responsible Person
    """

    class EntityIdentifier(str, Enum):
        """
        Code values for NM101
        """

        CASE_MANAGER = "6Y"
        KEY_PERSON = "9K"
        PERSON_LEGALLY_RESPONSIBLE_FOR_CHILD = "E1"
        EXECUTOR_OF_ESTATE = "EI"
        EX_SPOUSE = "EXS"
        OTHER_INSURED = "GB"
        GUARDIAN = "GD"
        POWER_OF_ATTORNEY = "J6"
        LEGAL_REPRESENTATIVE = "LR"
        RESPONSIBLE_PARTY = "QD"
        PARENT = "S1"
        SIGNIFICANT_OTHER = "TZ"
        SPOUSE = "X4"

    class IdentificationCodeQualifier(str, Enum):
        """
        Code values for NM108
        """

        SOCIAL_SECURITY_NUMBER = "34"
        MUTUALLY_DEFINED = "ZZ"

    entity_identifier_code: EntityIdentifier
    entity_type_qualifier: Literal["1"]
    name_last_or_organization_name: str = Field(min_length=1, max_length=60)
    identification_code_qualifier: Optional[IdentificationCodeQualifier]
    identification_code: Optional[str] = Field(min_length=2, max_length=80)


class Loop2100HNm1Segment(Nm1Segment):
    """
    Drop off location name
    """

    entity_identifier_code: Literal["45"]
    entity_type_qualifier: Literal["1"]


class Loop2200DtpSegment(DtpSegment):
    """
    Member disability dates
    """

    class DateTimeQualifier(str, Enum):
        """
        Code values for DTP01
        """

        INITIAL_DISABILITY_PERIOD_START = "360"
        INITIAL_DISABILITY_PERIOD_END = "361"


class Loop2300DtpSegment(DtpSegment):
    """
    Member coverage dates
    """

    class DateTimeQualifier(str, Enum):
        """
        Code values for DTP01
        """

        ENROLLMENT_EFFECTIVE_DATE = "300"
        MAINTENANCE_EFFECTIVE = "303"
        PREMIUM_PAID_TO_DATE_END = "343"
        BENEFIT_BEGIN = "348"
        BENEFIT_END = "349"
        LAST_PREMIUM_PAID_DATE = "543"
        PREVIOUS_PERIOD = "695"

    class DateTimePeriodFormatQualifier(str, Enum):
        """
        Code values for DTP02
        """

        SPECIFIC_DATE = "D8"
        DATE_RANGE = "RD8"

    date_time_qualifier: DateTimeQualifier
    date_time_period_format_qualifier: DateTimePeriodFormatQualifier
    date_time_period: str


class Loop2300AmtSegment(AmtSegment):
    """
    Member coverage amounts
    """

    class AmountQualifierCode(str, Enum):
        """
        Code values for AMT01
        """

        COINSURANCE_ACTUAL = "B9"
        COPAYMENT_AMOUNT = "C1"
        DEDUCTIBLE_AMOUNT = "D2"
        EXPECTED_EXPENDITURE_AMOUNT = "EBA"
        OTHER_UNLISTED_AMOUNT = "FK"
        PREMIMUM_AMOUNT = "P3"
        SPEND_DOWN = "R"

    amount_qualifier_code: AmountQualifierCode


class Loop2300RefSegment(RefSegment):
    """
    Member coverage reference identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        CLIENT_REPORTING_CATEGORY = "17"
        GROUP_OR_POLICY_NUMBER = "1L"
        PAYMENT_CATEGORY = "9V"
        CLASS_OF_CONTRACT_CODE = "CE"
        SERVICE_CONTRACT_NUMBER = "E8"
        MEDICAL_ASSISTANCE_CATEGORY = "M7"
        PROGRAM_IDENTIFICATION_NUMBER = "PID"
        RATE_CODE_NUMBER = "RB"
        INTERNAL_CODE_NUMBER = "X9"
        ISSUER_NUMBER = "XM"
        SPECIAL_PROGRAM_CODE = "XX1"
        SERVICE_AREA_CODE = "XX2"
        COUNTY_CODE = "ZX"
        MUTUALLY_DEFINED = "ZZ"
        UNIT_NUMBER = "QQ"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2310Nm1Segment(Nm1Segment):
    """
    Member Coverage Provider Information Place/Location
    """

    class EntityIdentifierCode(str, Enum):
        """
        Code values for NM101
        """

        LABORATORY = "1X"
        OBGYN_FACILITY = "3D"
        HOSPITAL = "80"
        FACILITY = "FA"
        DOCTOR_OF_OPTOMETRY = "OD"
        PRIMARY_CARE_PROVIDER = "P3"
        PHARMACY = "QA"
        DENTIST = "QN"

    class IdentificationCodeQualifier(str, Enum):
        """
        Code values for NM108
        """

        SOCIAL_SECURITY_NUMBER = "34"
        FEDERAL_TAXPAYER_IDENTIFICATION_NUMBER = "FI"
        SERVICE_PROVIDER_NUMBER = "SV"
        CMS_NPI = "XX"

    class EntityRelationshipCode(str, Enum):
        """
        Code values for NM110
        """

        ESTABLISHED_PATIENT = "25"
        NOT_ESTABLISHED_PATIENT = "26"
        UNKNOWN = "72"

    entity_identifier_code: EntityIdentifierCode
    identification_code_qualifier: Optional[IdentificationCodeQualifier]
    entity_relationship_code: Optional[EntityRelationshipCode]


class Loop2310PlaSegment(PlaSegment):
    """
    Member Coverage Provider Information Place/Location
    """

    class MaintenanceReasonCode(str, Enum):
        """
        Code values for PLA05
        """

        VOLUNTARY_WITHDRAWL = "14"
        PLAN_CHANGE = "22"
        CURRENT_CUSTOMER_INFORMATION_FILE_ERROR = "46"
        DISSATISFACTION_WITH_OFFICE_STAFF = "AA"
        DISSATISFACTION_WITH_MEDICAL_CARE_SERVICES = "AB"
        INCONVENIENT_OFFICE_LOCATION = "AC"
        DISSATISFACTION_WITH_OFFICE_HOURS = "AD"
        UNABLE_TO_SCHEDULE_APPOINTMENTS_IN_TIMELY_MANNER = "AE"
        DISSATISFACTION_WITH_PHYSICIANS_REFERRAL_POLICY = "AF"
        LESS_RESPECT_AND_ATTENTION_GIVEN_THAN_TO_OTHER_PATIENTS = "AG"
        PATIENT_MOVED_NEW_LOCATION = "AH"
        NO_REASON_GIVEN = "AI"
        APPOINTMENT_TIMES_NOT_MET_IN_TIMELY_MANNER = "AJ"

    action_code: Literal["2"]
    entity_identifier_code: Literal["1P"]
    maintenance_reason_code: MaintenanceReasonCode


class Loop2320RefSegment(RefSegment):
    """
    Member Coverage COB Reference Identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        ACCOUNT_SUFFIX_CODE = "60"
        GROUP_NUMBER = "6P"
        SOCIAL_SECURITY_NUMBER = "SY"
        MUTUALLY_DEFINED = "ZZ"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2320DtpSegment(DtpSegment):
    """
    Member Coverage COB Date Segment
    """

    class DateTimeQualifier(str, Enum):
        """
        Code values for DTP
        """

        COORDINATION_BENEFITS_BEGIN = "344"
        COORDINATION_BENEFITS_END = "345"

    date_time_qualifier: DateTimeQualifier
    date_time_period_format_qualifier: Literal["D8"]


class Loop2330Nm1Segment(Nm1Segment):
    """
    Member Coverage COB Related Entity
    """

    class EntityIdentifierCode(str, Enum):
        """
        Code values for NM101
        """

        EMPLOYER = "36"
        GROUP = "GW"
        INSURER = "IN"

    class IdentificationCodeQualifier(str, Enum):
        """
        Code values for NM108
        """

        FEDERAL_TAXPAYER_IDENTIFICATION = "FI"
        NAIC_IDENTIFICATION = "NI"
        CMS_PLAN_ID = "XV"

    entity_identifier_code: EntityIdentifierCode
    entity_type_qualifier: Literal["2"]
    name_last_or_organization_name: Optional[str] = Field(min_length=1, max_length=60)
    identification_code_qualifier: Optional[IdentificationCodeQualifier]


class Loop2330PerSegment(PerSegment):
    """
    Member Coverage COB Administrative Communications
    """

    contact_function_code: Literal["CN"]
    communication_number_qualifier_1: Literal["TE"]


class Loop2000LsSegment(LsSegment):
    """
    Additional reporting categories loop used to signal the start of the 2700 loop.
    """

    loop_id_code: Literal["2700"]


class Loop2750N1Segment(N1Segment):
    """
    Member Reporting Category
    """

    entity_identifier_code: Literal["75"]


class Loop2750RefSegment(RefSegment):
    """
    Member Reporting Category Reference Identification
    """

    class ReferenceIdentificationQualifier(str, Enum):
        """
        Code values for REF01
        """

        CONTRACTING_DISTRICT_NUMBER = "00"
        CLIENT_REPORTING_CATEGORY = "17"
        PLAN_NUMBER = "18"
        DIVISION_NUMBER = "19"
        UNION_NUMBER = "26"
        BRANCH_IDENTIFIER = "3L"
        APPLICATION_NUMBER = "6M"
        PAYMENT_CATEGORY = "9V"
        ACCOUNT_CATEGORY = "9X"
        GEOGRAPHIC_NUMBER = "GE"
        LOCATION_NUMBER = "LU"
        PROGRAM_IDENTIFICATION_NUMBER = "PID"
        SPECIAL_PROGRAM_CODE = "XX1"
        SERVICE_AREA_CODE = "XX2"
        GEOGRAPHIC_KEY = "YY"
        MUTUALLY_DEFINED = "ZZ"

    reference_identification_qualifier: ReferenceIdentificationQualifier


class Loop2750DtpSegment(DtpSegment):
    """
    Member Reporting Category Dates
    """

    class DateTimePeriodFormatQualifier(str, Enum):
        """
        Code values for DTP02
        """

        SPECIFIC_DATE = "D8"
        DATE_RANGE = "RD8"

    date_time_qualifier: Literal["007"]
    date_time_period: str


class Loop2000LeSegment(LeSegment):
    """
    Additional reporting categories loop termination, used to signal the end of the 2700 loop.

    """

    loop_id_code: Literal["2700"]
