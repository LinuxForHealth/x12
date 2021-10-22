"""
segments.py

Specialized segment models for the Health Care Claim Status Request 276 005010X212 transaction.
"""
from x12.segments import StSegment
from typing import Literal


class HeaderStSegment(StSegment):
    """
    Customized ST segment for 837 transaction header
    """

    transaction_set_identifier_code: Literal["276"]
    implementation_convention_reference: Literal["005010X212"]
