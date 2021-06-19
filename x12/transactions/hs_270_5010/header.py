"""
header.py

The Eligibility Inquiry/270 transaction header
"""

import datetime

from pydantic import BaseModel, Field
from x12.models import X12BaseSegmentModel
from typing import Literal, Optional


class StSegment(X12BaseSegmentModel):
    """
    Transaction header
    Example:
        ST*270*0001*005010X279A1~
    """
    code: Literal["270"]
    control_number: str = Field(min_length=4, max_length=9)
    implementation_reference: Literal["005010X279A1"]


class BhtSegment(X12BaseSegmentModel):
    """
    Defines the business application purpose and supporting reference data for the transaction.
    Example:
        BHT*0022*01**19980101*1400*RT~
    """
    structure_code: Literal["0022"]
    purpose_code: Literal["01", "13"]
    transactional_identifier: Optional[str] = Field(min_length=1, max_length=50)
    transaction_creation_date: datetime.date
    transaction_creation_time: datetime.time
    transaction_code: Optional[Literal["RT"]]


class Header(BaseModel):
    """
    The transaction header
    """
    st_segment: StSegment
    bht_segment: BhtSegment


