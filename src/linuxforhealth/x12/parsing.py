"""
parsing.py

Provides X12 segment parsing support.
"""
import inspect
import logging
import re
from abc import ABC
from collections import defaultdict
from functools import lru_cache, wraps
from importlib import import_module
from typing import Callable, Dict, List, Optional, Set

from .models import X12SegmentGroup, X12Segment, X12Delimiters
from .support import parse_x12_major_version

logger = logging.getLogger(__name__)

# naming convention for parsing functions:
# parse_nm1_segment, parse_st_segment, etc
PARSING_FUNCTION_REGEX = "set\\_(.)*\\_loop"

# the base transaction prefix used in _load functions
BASE_TRANSACTION_PREFIX = "linuxforhealth.x12.v"


def match(segment_name: str, conditions: Dict = None) -> Callable:
    """
    The match decorator matches a X12 segment to a decorated function.

    Decorated functions are expected to have the signature: func(context: X12ParserContext).

    The following example matches a NM1 (entity name) segment:

    @match("NM1")
    def the_func(context, segment_data):
       # evaluation occurs here

    The match decorator accepts additional criteria, or conditions, for segment matching. The criteria evaluates a
    matched segment fields using equality checks.

    The following examples matches a NM1 segment where the entity_type_qualifier field is equal to "2",
    or a non-person entity.

    @match("NM1", conditions={"entity_type_qualifier": "2"})
    def the_func(context, segment_data):
       # evaluation occurs here

    Finally, the decorator adds a "segment grouping" attribute to the decorated function to optimize lookups.

    :param segment_name: The X12 segment name
    :param conditions: Dictionary of conditions. Key = x12 segment field name, Value = field value
    """

    conditions = conditions or {}

    def decorator(f):
        # add a segment grouping attribute for the function
        f.segment_group = segment_name.upper()

        @wraps(f)
        def wrapped(segment_data: Dict, data_context: X12ParserContext):
            """
            Executes the wrapped function if segment_data matches the segment_name and optional conditions.

            :param segment_data: List of segment fields.
            :param data_context: The X12ParserContext object
            """
            is_matched = segment_name.upper() == segment_data["segment_name"].upper()

            if not is_matched:
                return
            elif is_matched and not conditions:
                return f(data_context, segment_data)
            else:
                for k, v in conditions.items():
                    # evaluate "one of" matches
                    if isinstance(v, list):
                        for i in v:
                            if segment_data[k].upper() == i.upper():
                                return f(data_context, segment_data)
                    else:
                        # evaluate single matches
                        if segment_data[k].upper() == v.upper():
                            return f(data_context, segment_data)

        return wrapped

    return decorator


class X12ParserContext:
    """
    The X12ParserContext maintains the current parsing position and provides a record cache.

    The parsing position is set using `set_loop_context`, which sets the current loop name and the data structure,
    usually a dictionary, for the loop.

    Cached records include:
    * The current subscriber record
    * The current patient record
    * The current hierarchical segment

    The current hierarchical segment is set in the core parser. Subscriber and patient records are set manually within a
    transaction's loop parser.

    Cached record usage varies based on transaction type.
    """

    @property
    def loop_name(self):
        """return the current loop name"""
        return None if not self.parsed_loops else self.parsed_loops[-1]

    def set_loop_context(self, loop_name: str, loop_container: Dict) -> None:
        """
        Sets the current loop context.

        The loop context includes a list of parsed loops and the loop "container". The "loop container" is expected to
        reference the larger transactional data structure.

        :param loop_name: The "current" loop name.
        :param loop_container: The "current" loop record.
        """

        self.parsed_loops.append(loop_name)
        self.loop_container = loop_container

    def reset_transaction(self) -> None:
        """Resets transactional attributes, including loop attributes."""

        self.parsed_loops.clear()
        self.loop_container.clear()
        self.transaction_data.clear()
        self.transaction_data["header"] = {}
        self.transaction_data["footer"] = {}
        self.is_transaction_complete = False
        self.subscriber_record = None
        self.patient_record = None
        self.hl_segment = None

    def mark_transaction_complete(self) -> None:
        """Marks the current transaction as complete"""

        self.is_transaction_complete = True

    def __init__(self) -> None:
        """
        Configures the X12ParseContext instance.
        The current transaction data record is initialized to include the header and footer keys used in all transaction
        models.
        """

        self.parsed_loops: List[str] = []
        self.loop_container: Optional[Dict] = {}
        self.transaction_data: Optional[Dict] = {"header": {}, "footer": {}}
        self.is_transaction_complete: bool = False
        self.subscriber_record: Optional[Dict] = None
        self.patient_record: Optional[Dict] = None
        self.hl_segment: Optional[Dict] = None


class X12Parser(ABC):
    """
    Parses X12 segments into a transactional model.
    """

    # parsing functions used to create loops in the transaction data model
    loop_parsers = None

    def _lookup_segment_model(self, segment_name) -> X12Segment:
        """
        Searches for a segment model by name.

        :param segment_name: The segment name
        :return: The segment model
        :raises: KeyError if the segment is not found
        """

        try:
            segment_model: Optional[X12Segment] = self._segment_models[segment_name]
        except KeyError:
            msg: str = f"Unsupported segment {segment_name}"
            logger.exception(msg)
            raise
        else:
            return segment_model

    def _get_segment_field_names(self, segment_name) -> List:
        """
        Returns the field names for a specific segment

        :param segment_name: The segment name
        """

        segment_model: X12Segment = self._lookup_segment_model(segment_name)
        # exclude "meta" fields such as delimiters that are not in the segment data
        field_names = [f for f in segment_model.__fields__ if f != "delimiters"]
        return field_names

    def _get_multivalue_fields(self, segment_name) -> Dict[str, str]:
        """
        Returns a dictionary of multi-value fields.
        Dictionary key is the field name, the value is the field separator.
        This dictionary is used to split fields appropriately before they are added to the transaction model.

        :param segment_name: The segment name
        :returns: a dictionary containing the multivalue fields and field separator
        """

        multivalue_fields: Dict = {}

        segment_model: X12Segment = self._lookup_segment_model(segment_name)

        for field_name, model_data in segment_model.__fields__.items():
            if field_name == "delimiters":
                continue

            if "typing.List" in str(model_data.outer_type_):
                is_component_field: bool = model_data.field_info.extra.get(
                    "is_component", False
                )
                if is_component_field:
                    multivalue_fields[field_name] = self._delimiters.component_separator
                else:
                    multivalue_fields[
                        field_name
                    ] = self._delimiters.repetition_separator

        return multivalue_fields

    def _parse_segment(self, segment_name: str, segment_fields: List[str]) -> Dict:
        """
        Parses a X12 segment field list into a data record (dictionary) with field names and values.
        The segment_field values are assigned to field names using the pydantic model for the transaction set.

        :param segment_name: The name of the X12 segment
        :param segment_fields: List of segment field values
        :return: The parsed data as a dictionary.
        """

        segment_data: Dict = {"delimiters": self._delimiters.dict()}
        field_names: List = self._get_segment_field_names(segment_name)
        multivalue_fields: Dict = self._get_multivalue_fields(segment_name)

        # segment_fields and field_name lengths may not match
        # drive the mapping with segment_fields as it includes all fields within the transactional context
        # field_names includes ALL available fields within the specification
        for index, value in enumerate(segment_fields):
            field_name: str = field_names[index]

            multivalue_separator: str = multivalue_fields.get(field_name)
            if multivalue_separator:
                value = value.split(multivalue_separator)

            segment_data[field_name] = value if value else None

        return segment_data

    def _is_final_segment(self, segment_name) -> bool:
        """Returns True if the segment name is the final segment in a transaction set."""

        return segment_name.lower() == "se"

    def load_model(self) -> X12SegmentGroup:
        """
        Loads the instance's data record into a X12 transactional model.

        :return: The X12 transactional model.
        """

        return self._transaction_model(**self._context.transaction_data)

    def parse(
        self, segment_name: str, segment_fields: List[str]
    ) -> Optional[X12SegmentGroup]:
        """
        Parses an X12 segment into the instance's data record attribute.

        Sets the following context attributes:
        * hl_segment

        Returns a X12 Transaction Model when all segments are received.

        :param segment_name: The name of the X12 segment (ST, HL, NM1, etc)
        :param segment_fields: List of segment field values
        :return: The X12 Transaction Model if ready, otherwise None.
        """

        model: Optional[X12SegmentGroup] = None

        # convert segment data to a dictionary "record"
        segment_data: Dict = self._parse_segment(segment_name, segment_fields)

        if segment_name.lower() == "hl":
            self._context.hl_segment = segment_data

        for loop_parser in self._loop_parsers[segment_name]:
            loop_parser(segment_data, self._context)

        segment_key = f"{segment_name.lower()}_segment"

        # write segment data
        # check for existing list entries for repeating segments
        existing_value = self._context.loop_container.get(segment_key)
        if existing_value is None:
            self._context.loop_container[segment_key] = segment_data
        elif isinstance(existing_value, list):
            self._context.loop_container[segment_key].append(segment_data)

        # close transaction set and return the model
        if self._is_final_segment(segment_name):
            self._context.mark_transaction_complete()
            model: X12SegmentGroup = self.load_model()
            self._context.reset_transaction()
            return model

    def __init__(
        self,
        transaction_model: X12SegmentGroup,
        loop_parsers: Dict,
        segment_models: Dict,
        x12_delimiters: Optional[X12Delimiters] = None,
    ) -> None:
        """
        Configures the parser instance

        :param transaction_model: The X12 transaction model.
        :param loop_parsers: The parser functions used to identify loop boundaries in the X12 transaction.
        :param segment_models: Dictionary mapping segment names to domain models
        :param x12_delimiters: The delimiters used to parse segments and fields.
        """
        self._transaction_model: X12SegmentGroup = transaction_model
        self._loop_parsers: Dict = loop_parsers
        self._segment_models: Dict = segment_models
        self._delimiters: X12Delimiters = x12_delimiters or X12Delimiters()
        self._context: X12ParserContext = X12ParserContext()


@lru_cache
def _load_loop_parsers(transaction_code: str, implementation_version) -> Dict:
    """Returns dictionary of Loop Parsers indexed by segment name"""
    pattern = re.compile(PARSING_FUNCTION_REGEX)
    loop_parsers = defaultdict(list)

    major_version = parse_x12_major_version(implementation_version)
    parsing_module = import_module(
        f"{BASE_TRANSACTION_PREFIX}{major_version}.x12_{transaction_code}_{implementation_version}.parsing"
    )

    funcs = [
        value
        for name, value in inspect.getmembers(parsing_module, inspect.isfunction)
        if pattern.match(name)
    ]

    for f in funcs:
        loop_parsers[f.segment_group].append(f)

    return loop_parsers


@lru_cache
def _load_transaction_model(
    transaction_code: str, implementation_version: str
) -> X12SegmentGroup:
    """Returns the transaction model for the x12 transaction"""

    major_version = parse_x12_major_version(implementation_version)

    transaction_module = import_module(
        f"{BASE_TRANSACTION_PREFIX}{major_version}.x12_{transaction_code}_{implementation_version}.transaction_set"
    )

    # return transaction set model
    for _, class_value in inspect.getmembers(transaction_module, inspect.isclass):
        if hasattr(class_value, "schema"):
            props: Set = set(class_value.schema()["properties"])
            # transaction set models have header and footer attributes
            if props.issuperset({"header", "footer"}):
                return class_value


@lru_cache
def _load_segment_lookup(implementation_version: str) -> Dict:
    """
    Returns a segment lookup dictionary for a specific implementation version.
    The lookup dictionary is implemented as Key = segment name, Value = segment model.
    The implementation version is the version identifier used in the ST03 - 005010X279A1, 005010X212, etc.

    :param implementation_version: The X12 implementation version used in ST03
    """
    major_version = parse_x12_major_version(implementation_version)
    module_name = f"{BASE_TRANSACTION_PREFIX}{major_version}.segments"
    segment_module = import_module(module_name)
    segment_lookup = [
        v for k, v in inspect.getmembers(segment_module) if k == "SEGMENT_LOOKUP"
    ][0]
    return segment_lookup


def create_parser(
    transaction_code: str, implementation_version: str, x12_delimiters: X12Delimiters
) -> X12Parser:
    """
    Creates a versioned X12 transaction parser.

    The parser includes "loop parsers" which initialize data structures for new loops as needed.

    :param transaction_code: The X12 transaction code (270, 271, 834, etc).
    :param implementation_version: The X12 implementation version (005010X279A1).
    :param x12_delimiters: The delimiters used to parse segments and fields.
    :raises: ModuleNotFoundError if the transaction module does not exist.
    :raises: ValueError if the transaction module exists, but a parser class cannot be found.
    """

    transaction_model: X12SegmentGroup = _load_transaction_model(
        transaction_code, implementation_version
    )
    loop_parsers: Dict = _load_loop_parsers(transaction_code, implementation_version)
    segment_lookup: Dict = _load_segment_lookup(implementation_version)
    return X12Parser(transaction_model, loop_parsers, segment_lookup, x12_delimiters)
