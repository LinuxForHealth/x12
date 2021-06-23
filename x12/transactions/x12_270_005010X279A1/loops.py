from x12.models import X12BaseLoopModel

"""
loops.py

Models the loops, or logical segment groupings, for the Eligibility 270 5010 transaction set.
LinuxForHealth X12 includes headers and footers within loops to standardize processing.
"""
from enum import Enum
from typing import Literal, Optional

from pydantic import Field, PositiveInt

from x12.segments import BhtSegment, HlSegment, StSegment


class BhtPurposeCode(str, Enum):
    """
    Code values for Header.BHT02
    """

    CANCELLATION = "01"
    REQUEST = "13"


class BhtTransactionCode(str, Enum):
    """
    Code values for Header.BHT06
    """

    SPEND_DOWN = "RT"


class HeaderBhtSegment(BhtSegment):
    """
    Customized BHT Segment for 270 transaction header
    """

    structure_code: Literal["0022"] = "0022"
    purpose_code: BhtPurposeCode
    transactional_identifier: str = Field(min_length=1, max_length=50)
    transaction_code: Optional[BhtTransactionCode]


class Loop2000AHlSegment(HlSegment):
    parent_id_number: Optional[PositiveInt]


class Header(X12BaseLoopModel):
    loop_name: str = "HEADER"
    st_segment: StSegment
    bht_segment: HeaderBhtSegment


class Loop2000A(X12BaseLoopModel):
    pass
