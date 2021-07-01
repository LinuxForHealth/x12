"""
parsing.py

Provides X12 segment parsing support.
"""
import inspect
import logging
import re
from abc import ABC, abstractmethod
from collections import defaultdict
from functools import lru_cache, wraps
from importlib import import_module
from typing import Callable, Dict, List, Optional

from x12.models import X12SegmentGroup
from x12.segments import SEGMENT_LOOKUP

logger = logging.getLogger(__name__)

# naming convention for parsing functions:
# parse_nm1_segment, parse_st_segment, etc
PARSING_FUNCTION_REGEX = "parse\\_(.)*\\_segment"


def match(segment_name: str, conditions: Dict[str, str] = None):
    """
    The match decorator matches a "parsed" X12 segment to a parsing function.

    Matches are made using the segment name and conditions (optional).
    Conditions are limited to equality checks.

    The decorator also adds a "segment grouping" attribute to the decorated function to optimize lookups.

    :param segment_name: The X12 segment name
    :param conditions: Dictionary of conditions. Key = x12 segment field name, Value = field value
    """
    conditions = conditions or {}

    def decorator(f):
        f.segment_group = segment_name.upper()

        @wraps(f)
        def wrapped(segment_data, data_context, data_record):
            if segment_name.upper() == segment_data["segment_name"].upper():
                unmatched = {
                    k: v
                    for k, v in conditions.items()
                    if segment_data[k].upper() != v.upper()
                }
                if len(unmatched) == 0:
                    f(segment_data, data_context, data_record)

        return wrapped

    return decorator


class X12SegmentParser(ABC):
    """
    Parses X12 segments into a transactional model.
    """

    @classmethod
    @lru_cache
    def load_parser(
        cls, transaction_code: str, implementation_version: str
    ) -> "X12SegmentParser":
        """
        Returns the parser for a specific X12 transaction and version.
        The parser includes specific parsers for each segment in the transaction set.

        :param transaction_code: The X12 transaction code (270, 271, 834, etc)
        :param implementation_version: The X12 implementation version (005010X279A1)
        :raises: ModuleNotFoundError if the transaction module does not exist.
        :raises: ValueError if the transaction module exists, but a parser class cannot be found.
        """
        transaction_package: str = f"x12_{transaction_code}_{implementation_version}"
        parser_package: str = f"x12.transactions.{transaction_package}.parse"
        mod = import_module(parser_package)

        def load_segment_parsers() -> Dict[str, List[Callable]]:
            """Returns dictionary of Segment Name [Key], Segment Parsers [List]"""
            p = re.compile(PARSING_FUNCTION_REGEX)
            segment_parsers = defaultdict(list)
            funcs = [
                value
                for name, value in inspect.getmembers(mod, inspect.isfunction)
                if p.match(name)
            ]

            for f in funcs:
                segment_parsers[f.segment_group].append(f)

            return segment_parsers

        # load parser class
        for class_name, class_value in inspect.getmembers(mod, inspect.isclass):
            if class_name != "X12SegmentParser" and hasattr(class_value, "parse"):
                class_value.segment_parsers = load_segment_parsers()
                return class_value()
        else:
            raise ValueError(
                f"Unable to load parser for {transaction_code} - {implementation_version}"
            )

    def _parse_segment(self, segment_name: str, segment_fields: List[str]) -> Dict:
        """
        Parses the X12 segment, which is a list of field values, into a data record (dictionary) with field names
        and values.

        :param segment_name: The name of the X12 segment
        :param segment_fields: List of segment field values
        :return: The parsed data as a dictionary.
        """
        try:
            segment_model: Optional[X12SegmentGroup] = self._segment_lookup[
                segment_name
            ]
        except KeyError:
            msg = f"Unsupported segment {segment_name}"
            logger.exception(msg)
            raise

        segment_data: Dict = {}
        field_names = [f for f in segment_model.__fields__ if f != "delimiters"]

        # segment_fields and field_name lengths may not match
        # drive the mapping with segment_fields as it includes all fields within the transactional context
        # field-names includes ALL available fields within the specification
        for index, value in enumerate(segment_fields):
            field_name = field_names[index]
            segment_data[field_name] = value

        return segment_data

    def _reset(self):
        """
        Resets the parser's state
        """
        self._context.clear()
        self._context["is_record_complete"] = False
        self._context["current_loop"] = None

        self._data_record.clear()
        self._data_record["header"] = {"st_segment": None}
        self._data_record["footer"] = {"se_segment": None}

    @abstractmethod
    def load_model(self) -> X12SegmentGroup:
        """
        Loads the instance's data record into a X12 transactional model.

        :return: The X12 transactional model.
        """
        pass

    def parse(
        self, segment_name: str, segment_fields: List[str]
    ) -> Optional[X12SegmentGroup]:
        """
        Parses an X12 segment into the instance's data record attribute.
        Returns the appropriate X12 Transaction Model when all segments are received.

        :param segment_name: The name of the X12 segment
        :param segment_fields: List of segment field values
        :return: The X12 Transaction Model if ready, otherwise None.
        """
        model: Optional[X12SegmentGroup] = None

        # convert segment data to a record
        segment_data = self._parse_segment(segment_name, segment_fields)
        # execute parsers
        for segment_parser in self.segment_parsers[segment_name]:
            segment_parser(segment_data, self._context, self._data_record)

            if self._context["is_record_complete"]:
                model = self.load_model()
                self._reset()
                return model

    def __init__(self):
        """
        Configures the data record for the parser instance
        """
        self._context: Dict = {"is_record_complete": False}
        self._data_record: Dict = {}
        self._segment_parsers: Dict = {}
        self._segment_lookup = SEGMENT_LOOKUP

        # resets state attributes to an initial condition
        self._reset()
