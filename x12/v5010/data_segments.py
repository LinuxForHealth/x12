"""
data_segments.py

Data models for X12 Segments used within a X12 5010 transaction set
"""
from x12.models import X12BaseSegmentModel
from pydantic import PositiveInt, Field
import datetime
from typing import Optional


class BhtSegment(X12BaseSegmentModel):
    """
    Defines Business Structure of a transaction set.
    Example:
    BHT*0019*00*44445*20040213*0932*CH~
    """
    hierarchical_structure_code: str = Field(min_length=4, max_length=4)
    purpose_code: str = Field(min_length=2, max_length=2)
    transaction_identifier: Optional[PositiveInt]
    transaction_set_creation_date: datetime.date
    transaction_type_code: Optional[str]
