"""
transaction_set.py

Defines the Health Care Claims Status 277 005010X212 transaction set model.
"""
from linuxforhealth.x12.models import X12SegmentGroup
from .loops import Header, Footer, Loop2000A
from typing import List
from pydantic import Field, root_validator
from linuxforhealth.x12.validators import validate_segment_count


class HealthCareClaimsStatusResponse(X12SegmentGroup):
    """
    The Health Care Claims Status Response transaction model - 277
    """

    header: Header
    loop_2000a: List[Loop2000A] = Field(min_items=1)
    footer: Footer

    _validate_segment_count = root_validator(allow_reuse=True)(validate_segment_count)
