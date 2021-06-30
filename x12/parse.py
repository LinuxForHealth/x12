"""
parse.py

Provides X12 segment parsing support.
"""
from abc import ABC, abstractmethod
from functools import wraps
from typing import Dict, Optional, List
from x12.models import X12SegmentGroup
from importlib import import_module
import inspect


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


class X12SegmentParser(ABC):
    """
    Parses X12 segments into a Pydantic Model
    """

    @classmethod
    def load_parser(
        cls, transaction_code: str, implementation_version: str
    ) -> "X12SegmentParser":
        """
        Returns the segment processor for a specific transaction and version.

        :param transaction_code: The X12 transaction code (270, 271, 834, etc)
        :param implementation_version: The X12 implementation version (005010X279A1)
        :raises: ModuleNotFoundError if the transaction module does not exist.
        :raises: ValueError if the transaction module exists, but a parser class cannot be found.
        """
        transaction_package: str = f"x12_{transaction_code}_{implementation_version}"
        parser_package: str = f"x12.transactions.{transaction_package}.parse"
        mod = import_module(parser_package)

        for attribute_name in dir(mod):
            attr = getattr(mod, attribute_name)
            if (
                inspect.isclass(attr)
                and attr.__name__ != "X12SegmentParser"
                and hasattr(attr, "parse")
            ):
                return attr
        else:
            raise ValueError(
                f"Unable to load parser for {transaction_code} - {implementation_version}"
            )

    @abstractmethod
    def parse_segment(self, segment: List[str]):
        """
        Parses the X12 segment into the parser's data record

        :param segment: The list of segment fields
        """
        pass

    @abstractmethod
    def is_record_complete(self, segment) -> bool:
        """
        Analyzes the current segment and data record to state to determine if a new record is created.

        :param segment: The current segment
        :return: True if the current segment is the start of a new record, otherwise False.
        """
        pass

    @abstractmethod
    def load_model(self) -> X12SegmentGroup:
        """Returns the Transaction Model for the parser instance"""
        pass

    def reset_data_record(self):
        """
        Resets the data record to include empty header and footer entries
        """
        self.data_record.clear()
        self.data_record["header"] = {"st_segment": None}
        self.data_record["footer"] = {"se_segment": None}

    def parse(self, segment: List[str]) -> Optional[X12SegmentGroup]:
        """
        Parses an X12 segment into the instance's data record attribute.
        Returns the appropriate X12 Transaction Model when all segments are received.

        :param segment: The segment to parse (list of fields)
        :return: The X12 Transaction Model if ready, otherwise None.
        """
        if self.is_record_complete(segment):
            model: X12SegmentGroup = self.load_model()
            self.reset_data_record()
            return model
        else:
            self.parse_segment(segment)
            return None

    def __init__(self):
        """
        Configures the data record for the parser instance
        """
        self.data_record: Dict = {}
        self.reset_data_record()
