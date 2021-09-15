"""
transaction_set.py

Defines the Professional Claims 837 005010X222A2 transaction set model.
"""

from x12.models import X12SegmentGroup
from .loops import Header, Footer


class HealthCareClaimProfessional(X12SegmentGroup):
    """
    The HealthCare Claim - Professional transaction model (837)
    """

    header: Header
    footer: Footer
