from x12.models import X12BaseSegmentModel
from pydantic import Field
import datetime


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


class StSegment(X12BaseSegmentModel):
    id: str
    control_number: str = Field(min_length=4, max_length=9)
    implementation_reference: str = Field(min_length=1, max_length=35)
