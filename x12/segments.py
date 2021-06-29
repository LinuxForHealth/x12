"""
segments.py

Models data segments used within X12 transactions.
A data segment is a "record" which contains related data elements, or fields.
"""
import datetime
from enum import Enum
from typing import List, Literal, Optional

from pydantic import Field, PositiveInt

from x12.models import X12BaseSegment


class BhtSegment(X12BaseSegment):
    """
    Defines the business application purpose and supporting reference data for the transaction.
    Example:
        BHT*0022*01**19980101*1400*RT~
    """

    segment_name: Literal["BHT"]
    hierarchical_structure_code: str = Field(min_length=4, max_length=4)
    transaction_set_purpose_code: str = Field(min_length=2, max_length=2)
    submitter_transactional_identifier: str = Field(min_length=1, max_length=50)
    transaction_set_creation_date: datetime.date
    transaction_set_creation_time: datetime.time
    transaction_type_code: str


class GeSegment(X12BaseSegment):
    """
    Defines a functional header for the message and is an EDI control segment.
    Example:
        GE*1*1~
    """

    segment_name: Literal["GE"]
    number_of_transaction_sets_included: PositiveInt
    group_control_number: str = Field(min_length=1, max_length=9)


class GsSegment(X12BaseSegment):
    """
    Defines a functional header for the message and is an EDI control segment.
    Example:
        GS*HS*000000005*54321*20131031*1147*1*X*005010X279A~
    """

    segment_name: Literal["GS"]
    functional_identifier_code: str = Field(min_length=2, max_length=2)
    application_sender_code: str = Field(min_length=2, max_length=15)
    application_receiver_code: str = Field(min_length=2, max_length=15)
    functional_group_creation_date: datetime.date
    functional_group_creation_time: datetime.time
    group_control_number: str = Field(min_length=1, max_length=9)
    responsible_agency_code: Literal["X"]
    version_identifier_code: str = Field(min_length=1, max_length=12)


class HlSegment(X12BaseSegment):
    """
    Defines a hierarchical organization used to relate one grouping of segments to another
    Example:
        HL*3*2*22*1~
    """

    segment_name: Literal["HL"]
    hierarchical_id_number: str = Field(min_length=1, max_length=12)
    hierarchical_parent_id_number: str = Field(min_length=1, max_length=12)
    hierarchical_level_code: str = Field(min_length=1, max_length=2)
    hierarchical_child_code: str = Field(min_length=1, max_length=1)


class IeaSegment(X12BaseSegment):
    """
    Defines the interchange footer and is an EDI control segment.
    Example:
        IEA*1*000000907~
    """

    segment_name: Literal["IEA"]
    number_of_included_functional_groups: PositiveInt
    interchange_control_number: str = Field(min_length=9, max_length=9)


class IsaSegment(X12BaseSegment):
    """
    Defines the interchange header and is an EDI control segment.
    The ISA Segment is a fixed length segment (106 characters)
    Example:
        ISA*03*9876543210*01*9876543210*30*000000005      *30*12345          *131031*1147*^*00501*000000907*1*T*:~
    """

    segment_name: Literal["ISA"]
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

    def x12(self) -> str:
        """
        Overriden to support ISA Segment specific date formatting
        """
        x12_str: str = super().x12()

        x12_fields: List[str] = x12_str.split(self.delimiters.element_separator)
        x12_fields[9] = x12_fields[9][2:]
        x12_fields[10] = x12_fields[10][0:4]

        x12_str = self.delimiters.element_separator.join(x12_fields)
        return x12_str


class Nm1Segment(X12BaseSegment):
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

    segment_name: Literal["NM1"]
    entity_identifier_code: str = Field(min_length=2, max_length=3)
    entity_type_qualifier: EntityQualifierCode
    name_last_or_organization_name: str = Field(min_length=1, max_length=60)
    name_first: Optional[str] = Field(min_length=1, max_length=35)
    name_middle: Optional[str] = Field(min_length=1, max_length=25)
    # not used
    name_prefix: Optional[str]
    name_suffix: Optional[str] = Field(min_length=1, max_length=10)
    identification_code_qualifier: str = Field(min_length=1, max_length=2)
    identification_code: str = Field(min_length=2, max_length=80)
    # NM110 - NM112 are not used


class SeSegment(X12BaseSegment):
    """
    Transaction Set Footer
    Example:
        SE*17*0001~
    """

    segment_name: Literal["SE"]
    transaction_segment_count: PositiveInt
    transaction_set_control_number: str = Field(min_length=4, max_length=9)


class StSegment(X12BaseSegment):
    """
    Transaction Set Header.
    Example:
        ST*270*0001*005010X279A1~
    """

    segment_name: Literal["ST"]
    transaction_set_identifier_code: str = Field(min_length=3, max_length=3)
    transaction_set_control_number: str = Field(min_length=4, max_length=9)
    implementation_convention_reference: str = Field(min_length=1, max_length=35)
