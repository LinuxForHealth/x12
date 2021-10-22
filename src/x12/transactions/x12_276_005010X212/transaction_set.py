"""
transaction_set.py

Defines the Health Care Claims Status 276 005010X212 transaction set model.
"""
from x12.models import X12SegmentGroup
from .loops import Header, Footer


class HealthCareClaimsStatusRequest(X12SegmentGroup):
    """
    The Health Care Claims Status transaction model - 276
    """

    header: Header
    footer: Footer
