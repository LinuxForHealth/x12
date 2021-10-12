"""
transaction_set.py

Defines the Health Care Claims Payment 835 005010X221A1 transaction set model.
"""
from x12.models import X12SegmentGroup
from .loops import Header, Footer, Loop1000A
from pydantic import root_validator
from x12.validators import validate_segment_count


class HealthCareClaimPayment(X12SegmentGroup):
    """
    The Health Care Claim Payment/835 transaction
    """

    header: Header
    loop_1000a: Loop1000A
    footer: Footer

    _validate_segment_count = root_validator(allow_reuse=True)(validate_segment_count)
