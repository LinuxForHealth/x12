"""
transaction_set.py

Defines the Health Care Claims Payment 835 005010X221A1 transaction set model.
"""
from x12.models import X12SegmentGroup
from .loops import Header, Footer, Loop1000A, Loop1000B, Loop2000
from pydantic import root_validator
from x12.validators import validate_segment_count
from typing import List, Set


class HealthCareClaimPayment(X12SegmentGroup):
    """
    The Health Care Claim Payment/835 transaction
    """

    header: Header
    loop_1000a: Loop1000A
    loop_1000b: Loop1000B
    loop_2000: List[Loop2000]
    footer: Footer

    _validate_segment_count = root_validator(allow_reuse=True)(validate_segment_count)

    @root_validator()
    def validate_lx_header(cls, values):
        """
        Validates that LX numbers within a transaction set are unique.
        """
        numbers: Set = set()
        for loop in values.get("loop_2000", []):
            n: int = loop.lx_segment.assigned_number
            if n in numbers:
                raise ValueError(f"duplicate assigned_numbers {n}")
            numbers.add(n)

        return values

    @property
    def payer(self):
        """Returns the Claim Payer"""
        return self.loop_1000a.dict()

    @property
    def payee(self):
        """Returns the Claim Payee receiving payment"""
        return self.loop_1000b.dict()

    @property
    def claim(self, return_first=True):
        """Returns the Claim Payment Information"""
        result = []
        for header in self.loop_2000:
            for claim in header.loop_2100:
                result.append(claim.dict())
        return result[0] if return_first else result
