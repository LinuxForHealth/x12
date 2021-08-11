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
from typing import Dict, Union
from collections import defaultdict
from datetime import datetime
from x12.support import parse_x12_date, count_segments


def validate_duplicate_ref_codes(cls, values: Dict):
    """
    Validates that a loop does not contain duplicate REF codes.

    :param values: The validated transaction data.
    :raises: ValueError if duplicate REF codes are found.
    """
    ref_codes = defaultdict(int)
    for ref_segment in values.get("ref_segment", []):
        # account for differing internal representation: model vs dict
        if not isinstance(ref_segment, dict):
            ref_segment = ref_segment.dict()

        ref_code = ref_segment.get("reference_identification_qualifier")
        ref_codes[ref_code] += 1
    duplicate_codes = {k for k, v in ref_codes.items() if v > 1}

    if duplicate_codes:
        raise ValueError(f"Duplicate REF codes {duplicate_codes}")
    return values


def validate_date_field(cls, v, values: Dict) -> Union[datetime.date, str, None]:
    """
    Validates a date field using the segment's date_time_period_format_qualifier (D8 or RD8).
    The date_time_period_format_qualifier is used to indicate if a date field is a specific date or a date range.
    Specific dates are have a "D8" qualifier value, while date ranges are qualified using "RD8".

    :param v: The date field value
    :param values: The segment's valid values.
    :return: The validated date field value
    :raises: ValueError if the date field value is an invalid format.
    """
    from x12.segments import DtpSegment

    def handle_x12_date(date_string: str):
        """Parses a x12 date string, raising a ValueError if an error occurs"""
        try:
            return parse_x12_date(date_string)
        except ValueError:
            raise ValueError(f"Invalid date value {date_string}")

    qualifier = values.get("date_time_period_format_qualifier")

    # the date field may be "optional" in which case the qualifier is not present
    # if the qualifier field is required, it will be validated at the field level
    if not qualifier:
        return v

    if (
        qualifier == DtpSegment.DateTimePeriodFormatQualifier.DATE_RANGE
        and "-" not in v
    ):
        raise ValueError(f"Invalid date range {v}")
    elif qualifier == DtpSegment.DateTimePeriodFormatQualifier.DATE_RANGE:
        for d in v.split("-"):
            handle_x12_date(d)
        return v
    else:
        return handle_x12_date(v)


def validate_segment_count(cls, values) -> Dict:
    """
    Validates the segment count conveyed in the transaction set footer, or SE segment.
    This function is only able to count "valid" segments since it is invoked as a "post" validator.

    :param values: The valid transaction set values.
    """
    expected_count: int = values["footer"].se_segment.transaction_segment_count

    if not expected_count:
        raise ValueError("Expected transaction count not found in SE segment")

    actual_count: int = count_segments(values)

    if expected_count != actual_count:
        raise ValueError(
            f"SE segment count {expected_count} != actual count {actual_count}"
        )

    return values
