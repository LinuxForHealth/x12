"""
transaction_set.py

Defines the Enrollment 834 005010X220A1 transaction set model.
"""

from typing import List, Dict, Tuple

from linuxforhealth.x12.models import X12SegmentGroup

from .loops import Footer, Header
from pydantic import root_validator
from linuxforhealth.x12.validators import validate_segment_count


class BenefitEnrollmentAndMaintenance(X12SegmentGroup):
    """
    The ASC X12 834 (Benefit Enrollment and Maintenance) transaction model.
    """

    header: Header
    footer: Footer

    _validate_segment_count = root_validator(allow_reuse=True)(validate_segment_count)
