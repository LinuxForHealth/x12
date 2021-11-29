"""
validators.py

Common/shared validators which may be reused in transaction sets.
"""
from pydantic import validator


@validator("hierarchical_parent_id_number", allow_reuse=True)
def validate_hl_parent_id(cls, field_value):
    """
    Validates the top level HL segment to ensure that the segment does not have a parent id.
    This validation is utilized withing hierarchical transactions such as the 270/271 (eligibility)
    and 276/277 (claims status).
    """
    if field_value:
        raise ValueError(f"invalid hierarchical_parent_id_number {field_value}")
    return field_value
