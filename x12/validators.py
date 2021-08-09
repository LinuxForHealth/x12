"""
validators.py

The validator functions in this module are reused across loops within a X12 transaction model.

Root validators have the signature (cls, values).

Field validators support a varying signature:
    - (cls, v) - where "v" is the value to validate
    - (cls, v, values) - where "values" are previously validated fields (dict)
    - (cls, v, values, config) - where "config" is the model config
    - (cls, kwargs) - provides a key word arguments shorthand for the above parameters
"""
from typing import Dict
from collections import defaultdict


def validate_duplicate_ref_codes(cls, values: Dict):
    """
    Validates that a loop does not contain duplicate REF codes.

    :param values: The raw, unvalidated transaction data.
    """
    ref_codes = defaultdict(int)
    for ref_segment in values.get("ref_segment", []):
        ref_code = ref_segment.get("reference_identification_qualifier")
        ref_codes[ref_code] += 1
    duplicate_codes = {k for k, v in ref_codes.items() if v > 1}

    if duplicate_codes:
        raise ValueError(f"Duplicate REF codes {duplicate_codes}")
    return values
