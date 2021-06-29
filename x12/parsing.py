"""
parsing.py
"""
import abc
from functools import wraps
from typing import Dict


def match(segment_name: str, conditions: Dict[int, str] = None):
    """
    The match decorator matches a X12 segment to a parsing rule using the segment name and optional conditions.
    Conditions are limited to equality checks.
    The decorator also adds a "segment grouping" attribute to the decorated function to optimize lookup times.
    :param segment_name: The X12 segment name
    :param conditions: Dictionary of conditions. Key = x12 segment field index, Value = field value
    """
    conditions = conditions or {}

    def decorator(f):
        f.segment_group = segment_name.upper()

        @wraps(f)
        def wrapped(segment_data, data_context, data_cache):
            if segment_name.upper() == segment_data[0].upper():
                unmatched = {
                    k: v
                    for k, v in conditions.items()
                    if segment_data[k].upper() != v.upper()
                }
                if len(unmatched) == 0:
                    f(segment_data, data_context, data_cache)

        return wrapped

    return decorator


class X12SegmentParser(abc.ABC):
    """
    Parses X12 segments into a Pydantic Model
    """

    pass
