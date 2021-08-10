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
import functools

from pydantic import Field, PositiveInt, condecimal, validator, root_validator

from x12.models import X12Segment, X12SegmentName
from x12.support import parse_x12_date, parse_x12_time, parse_interchange_date
from x12.validators import validate_date_field

# partial function used to "register" common field validator functions
# common validator functions have the sigature (cls, v, values)
field_validator = functools.partial(validator, pre=True, allow_reuse=True)


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
    transaction_set_creation_date: datetime.date
    transaction_set_creation_time: datetime.time
    transaction_type_code: str = Field(min_length=2, max_length=2)

    _validate_transaction_date = field_validator("transaction_set_creation_date")(parse_x12_date)
    _validate_transaction_time = field_validator("transaction_set_creation_time")(parse_x12_time)


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
    date_time_period: Optional[datetime.date]
    gender_code: Optional[GenderCode]

    _validate_x12_date = field_validator("date_time_period")(validate_date_field)

    @root_validator(pre=True)
    def validate_date_time_fields(cls, values):
        """
        Validates that both a date_time_period_format_qualifier and date_time_period are provided if one or the other is present

        :param values: The raw, unvalidated transaction data.
        """
        date_fields: Tuple = values.get("date_time_period_format_qualifier"), values.get(
            "date_time_period"
        )

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
    date_time_period: Union[datetime.date, str]

    _validate_x12_date = field_validator("date_time_period")(validate_date_field)


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

    @root_validator(pre=True)
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
    functional_group_creation_date: datetime.date
    functional_group_creation_time: datetime.time
    group_control_number: str = Field(min_length=1, max_length=9)
    responsible_agency_code: Literal["X"]
    version_identifier_code: str = Field(min_length=1, max_length=12)

    _validate_creation_date = field_validator("functional_group_creation_date")(parse_x12_date)
    _validate_creation_time = field_validator("functional_group_creation_time")(parse_x12_time)


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

    segment_name: X12SegmentName = X12SegmentName.III
    code_list_qualifier_code: str = Field(min_length=1, max_length=3)
    industry_code: str = Field(min_length=1, max_length=30)


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
    member_death_date: Optional[datetime.date]
    confidentiality_code: Optional[str] = Field(min_length=1, max_length=1)
    city_name: Optional[str] = Field(min_length=2, max_length=30)
    state_province_code: Optional[str] = Field(min_length=2, max_length=2)
    country_code: Optional[str] = Field(min_length=2, max_length=3)
    birth_sequence_number: Optional[int]

    _validate_death_date = field_validator("member_death_date")(validate_date_field)

    @root_validator(pre=True)
    def validate_member_death_datefields(cls, values):
        """
        Validates that both a date_time_period_format_qualifier and member_death_date are provided if one or the other is present

        :param values: The raw, unvalidated transaction data.
        """
        date_fields: Tuple = values.get("date_time_period_format_qualifier"), values.get(
            "member_death_date"
        )

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
    interchange_date: datetime.date
    interchange_time: datetime.time
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

    @root_validator(pre=True)
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

    @root_validator(pre=True)
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

    @root_validator(pre=True)
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

    @root_validator(pre=True)
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
