"""
support.py

Convenience functions for X12 Processing.
"""
import datetime
import functools
import os
from typing import Union, Dict

from pydantic import validator, BaseModel

from .config import IsaDelimiters


def is_x12_data(input_data: str) -> bool:
    """
    Returns True if the input data appears to be a X12 message.

    :param input_data: Input data to evaluate
    :return: True if the input data is a x12 message, otherwise False
    """

    return input_data.startswith("ISA") if input_data else False


def is_x12_file(file_path: str) -> bool:
    """
    Returns true if the file path exists and is a x12 file.
    Environment and user variables are expanded within the file path.

    :param file_path: The file path to test.
    :return: True if the file path is a x12 file, otherwise false
    """

    if not file_path:
        return False

    expanded_path = os.path.expandvars(os.path.expanduser(file_path))
    if not os.path.exists(expanded_path) or os.path.isdir(expanded_path):
        return False

    with (open(expanded_path, "r")) as f:
        f.seek(0)
        # ISA segment is first 106 characters
        isa_segment = f.read(IsaDelimiters.SEGMENT_LENGTH)
        return is_x12_data(isa_segment)


def parse_interchange_date(date_string: str) -> datetime.date:
    """Parses a datetime.date from date fields in the ISA (interchange) segment"""

    return datetime.datetime.strptime(date_string, "%y%m%d").date()


def parse_x12_date(date_string: str) -> Union[datetime.date, datetime.datetime, None]:
    """Parses a datetime.date or datetime.datetime from date fields in X12 transaction segments"""
    parsed_date = None

    if not date_string:
        return parsed_date

    if len(date_string) == 8:
        # date
        parsed_date = datetime.datetime.strptime(date_string, "%Y%m%d").date()
    elif len(date_string) == 12:
        # date and time
        parsed_date = datetime.datetime.strptime(date_string, "%Y%m%d%H%M")

    return parsed_date


def count_segments(values: Dict) -> int:
    """
    Returns the number of segment records contained within a X12 data model.

    The X12 data model's top level structure includes the following keys:
    * header
    * <top level loop>:
    * footer
    The top level keys may contain additional nested structures which contain "segment" keys such as
    nm1_segment, st_segment, dtp_segment, se_segment, etc.

    :param values: The validated model values
    :returns: the total segment count
    """
    segment_count: int = 0

    for k, v in values.items():
        if k.endswith("_segment") and isinstance(v, dict):
            segment_count += 1
        elif k.endswith("_segment") and isinstance(v, list):
            segment_count += len(v)
        elif isinstance(v, BaseModel):
            segment_count += count_segments(v.dict())
        elif isinstance(v, list):
            for item in v:
                segment_count += (
                    count_segments(item.dict())
                    if hasattr(item, "dict")
                    else count_segments(item)
                )
        elif isinstance(v, dict):
            segment_count += count_segments(v)

    return segment_count


def parse_x12_major_version(x12_implementation_version) -> str:
    """
    Parses the x12 major version from an implementation version string.
    If the version is invalid, an empty string is returned.

    Example:
        x = parse_x12_major_version("005010X279A1")
        print(x)
        # prints 5010

        x = parse_x12_major_version("00501")
        print(x)
        # prints ""

    :param x12_implementation_version: The X12 implementation version typically conveyed in ST03
    :returns: The x12 major version or an empty string
    """
    if x12_implementation_version is None or len(x12_implementation_version) < 6:
        return ""

    return x12_implementation_version[2:6]


# partial function used to "register" common field validator functions
# common validator functions have the signature (cls, v, values)
field_validator = functools.partial(validator, allow_reuse=True)
