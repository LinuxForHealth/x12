"""
transaction_set.py

Defines the Professional Claims 837 005010X222A2 transaction set model.
"""

from x12.models import X12SegmentGroup
from .loops import Header, Footer, Loop1000A, Loop1000B, Loop2000A, Loop2300
from pydantic import Field, root_validator
from typing import List, Dict
from x12.validators import validate_segment_count


class HealthCareClaimProfessional(X12SegmentGroup):
    """
    The HealthCare Claim - Professional transaction model (837)
    """

    header: Header
    loop_1000a: Loop1000A
    loop_1000b: Loop1000B
    loop_2000a: List[Loop2000A] = Field(min_items=1)
    footer: Footer

    _validate_segment_count = root_validator(allow_reuse=True)(validate_segment_count)

    @property
    def patient(self, return_first=True):
        """
        Returns patient demographics for the health care claim
        """
        result = []
        for billing_provider in self.loop_2000a:
            for subscriber in billing_provider.loop_2000b:
                if subscriber.hl_segment.hierarchical_child_code == "0":
                    result.append(
                        subscriber.dict(
                            exclude={"loop_2010bb", "loop_2300", "loop_2000c"}
                        )
                    )
                else:
                    for dependent in subscriber.loop_2000c:
                        result.append(dependent.dict(exclude={"loop_2300"}))

        return result[0] if return_first else result

    def _parse_claim_data(self, loop_2300: Loop2300) -> Dict:
        """Returns the claim"""

        claim_data = {"clm_segment": loop_2300.clm_segment.dict(), "sv1_segment": []}

        for service_line in loop_2300.loop_2400:
            claim_data["sv1_segment"].append(service_line.sv1_segment)

        return claim_data

    @property
    def claim(self, return_first=True):
        """
        Returns the header and line items for the health care claim
        """
        result = []
        for billing_provider in self.loop_2000a:
            for subscriber in billing_provider.loop_2000b:
                if subscriber.hl_segment.hierarchical_child_code == "0":
                    for claim in subscriber.loop_2300:
                        result.append(self._parse_claim_data(claim))
                else:
                    for dependent in subscriber.loop_2000c:
                        for claim in dependent.loop_2300:
                            result.append(self._parse_claim_data(claim))

        return result[0] if return_first else result
