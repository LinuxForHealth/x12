import datetime
from typing import Optional

from pydantic import Field, PositiveInt, conint

from x12.models import X12BaseSegmentModel


class BhtSegment(X12BaseSegmentModel):
    """
    Defines the business application purpose and supporting reference data for the transaction.
    Example:
        BHT*0022*01**19980101*1400*RT~
    """

    structure_code: str
    purpose_code: str
    transactional_identifier: str = Field(min_length=1, max_length=50)
    transaction_creation_date: datetime.date
    transaction_creation_time: datetime.time
    transaction_code: str


class GeSegment(X12BaseSegmentModel):
    """
    Defines a functional header for the message and is an EDI control segment.
    Example:
        GE*1*1~
    """

    transaction_count: PositiveInt
    control_number: str = Field(min_length=1, max_length=9)


class GsSegment(X12BaseSegmentModel):
    """
    Defines a functional header for the message and is an EDI control segment.
    Example:
        GS*HS*000000005*54321*20131031*1147*1*X*005010X279A~
    """

    id_code: str = Field(min_length=2, max_length=2)
    sender_code: str = Field(min_length=2, max_length=15)
    receiver_code: str = Field(min_length=2, max_length=15)
    creation_date: datetime.date
    creation_time: datetime.time
    control_number: str = Field(min_length=1, max_length=9)
    responsible_agency_code: str = Field(min_length=1, max_length=2)
    version_code: str = Field(min_length=1, max_length=12)


class HlSegment(X12BaseSegmentModel):
    """
    Defines a hierarchical organization used to relate one grouping of segments to another
    Example:
        HL*3*2*22*1~
    """
    id_number: PositiveInt
    parent_id_number: PositiveInt
    level_code: PositiveInt
    child_code: conint(ge=0, le=1)


class IeaSegment(X12BaseSegmentModel):
    """
    Defines the interchange footer and is an EDI control segment.
    Example:
        IEA*1*000000907~
    """

    group_count: PositiveInt
    control_number: str = Field(min_length=9, max_length=9)


class IsaSegment(X12BaseSegmentModel):
    """
    Defines the interchange header and is an EDI control segment.
    The ISA Segment is a fixed length segment (106 characters)
    Example:
        ISA*03*9876543210*01*9876543210*30*000000005      *30*12345          *131031*1147*^*00501*000000907*1*T*:~
    """

    auth_qualifier: str = Field(min_length=2, max_length=2)
    auth_information: str = Field(min_length=10, max_length=10)
    security_qualifier: str = Field(min_length=2, max_length=2)
    security_information: str = Field(min_length=10, max_length=10)
    sender_qualifier: str = Field(min_length=2, max_length=2)
    sender_id: str = Field(min_length=15, max_length=15)
    receiver_qualifier: str = Field(min_length=2, max_length=2)
    receiver_id: str = Field(min_length=15, max_length=15)
    interchange_date: datetime.date
    interchange_time: datetime.time
    repetition_separator: str = Field(min_length=1, max_length=1)
    control_version: str = Field(min_length=5, max_length=5)
    control_number: str = Field(min_length=9, max_length=9)
    acknowledgment_requested: str = Field(min_length=1, max_length=1)
    interchange_usage: str = Field(min_length=1, max_length=1)


class Nm1Segment(X12BaseSegmentModel):
    """
    Entity Name and Identification Number
    Example:
        NM1*PR*2*PAYER C*****PI*12345~
    """
    entity_identifier_code: str = Field(min_length=2, max_length=3)
    entity_type_qualifier: str = conint(ge=1, le=2)
    name_last_org_name: str = Field(min_length=1, max_length=60)
    first_name: Optional[str] = Field(min_length=1, max_length=35)
    middle_name: Optional[str] = Field(min_length=1, max_length=25)
    # not used
    prefix: str = ""
    suffix: Optional[str] = Field(min_length=1, max_length=10)
    code_qualifier: str = Field(min_length=1, max_length=2)
    identification_code: str = Field(min_length=2, max_length=80)
    # NM110 - NM112 are not used


class SeSegment(X12BaseSegmentModel):
    """
    Transaction Set Footer
    Example:
        SE*17*0001~
    """

    segment_count: PositiveInt
    control_number: str = Field(min_length=4, max_length=9)


class StSegment(X12BaseSegmentModel):
    """
    Transaction Set Header.
    Example:
        ST*270*0001*005010X279A1~
    """

    id: str
    control_number: str = Field(min_length=4, max_length=9)
    implementation_reference: str = Field(min_length=1, max_length=35)
