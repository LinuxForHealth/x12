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
        DISSATISFACTION_WITH_MEDICAL_CARE_SERVICES = "AA"
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
