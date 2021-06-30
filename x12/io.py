"""
io.py

Supports X12 I/O operations such as reading, writing, and modeling raw models.
"""
from io import StringIO, TextIOBase
from typing import Iterator, List, NoReturn, Optional, Tuple, Dict

from x12.config import IsaDelimiters, get_config
from x12.models import X12Delimiters, X12SegmentName, X12SegmentGroup, X12Segment
from x12.support import is_x12_data, is_x12_file
from x12.parse import X12SegmentParser
from x12.segments import SEGMENT_LOOKUP
import logging

logger = logging.getLogger(__name__)


class X12SegmentReader:
    """
    Streams segments from a X12 message or file.

    with X12Reader(x12_data) as r:
       for segment_name, segment, context in r.models():
          # do something interesting

    Segments are streamed in order using a buffered generator function.
    The buffer size is configured using the config/env variable X12_READER_BUFFER_SIZE which defaults to 1MB.
    """

    def __init__(self, x12_input: str):
        """
        Initializes the X12SegmentReader with a x12 input.
        The x12 input may be a message payload or a path to a x12 file.

        :param x12_input: The X12 Message or a path to a X12 file
        """

        self._x12_input: str = x12_input
        self._delimiters: X12Delimiters = X12Delimiters()

        # set in __enter__
        self._buffer_size: Optional[int] = None
        self._x12_stream: Optional[TextIOBase] = None

    def _parse_isa_segment(self) -> NoReturn:
        """
        Parses fields from the ISA segment to set delimiters/instance attributes.
        The ISA segment is conveyed in the first 106 characters of the transmission.
        """
        self._x12_stream.seek(0)

        isa_segment: str = self._x12_stream.read(IsaDelimiters.SEGMENT_LENGTH)
        self._delimiters.element_separator = isa_segment[
            IsaDelimiters.ELEMENT_SEPARATOR
        ]
        self._delimiters.repetition_separator = isa_segment[
            IsaDelimiters.REPETITION_SEPARATOR
        ]
        self._delimiters.segment_terminator = isa_segment[
            IsaDelimiters.SEGMENT_TERMINATOR
        ]
        self._delimiters.component_separator = isa_segment[
            IsaDelimiters.COMPONENT_SEPARATOR
        ]

    def __enter__(self) -> "X12SegmentReader":
        """
        Initializes the X12 Stream and parses messages delimiters from the ISA segment.
        :return: The X12SegmentReader instance
        :raise: ValueError if the x12 input is invalid
        """
        if is_x12_file(self._x12_input):
            self._x12_stream = open(self._x12_input, "r")
        elif is_x12_data(self._x12_input):
            self._x12_stream = StringIO(self._x12_input)
        else:
            raise ValueError(
                "Invalid x12_input. Expecting X12 Message or valid path to X12 File"
            )

        self._buffer_size: int = get_config().x12_reader_buffer_size

        self._x12_stream.seek(0)
        if not self._x12_stream.read(IsaDelimiters.SEGMENT_LENGTH):
            raise ValueError("Invalid X12Stream")

        self._parse_isa_segment()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> NoReturn:
        """
        Closes the X12SegmentReader's X12 Stream and sets instance attributes to None
        :param exc_type: Exception Type
        :param exc_val: Exception Value
        :param exc_tb: Exception traceback
        """
        if not self._x12_stream.closed:
            self._x12_stream.close()

        self._delimiters = None
        self._x12_input = None

    def segments(self) -> Iterator[Tuple[str, List[str]]]:
        """
        Iterator function used to return X12 models from the underlying X12 stream.
        The read buffer size may be configured using X12_READER_BUFFER_SIZE.
        :return: Iterator containing segment name and segment fields.
        """
        self._x12_stream.seek(0)
        while True:
            buffer: str = self._x12_stream.read(self._buffer_size)

            if not buffer:
                break

            while buffer[-1] != self._delimiters.segment_terminator:
                next_character: str = self._x12_stream.read(1)
                if not next_character:
                    break
                buffer += next_character

            # buffer cleanup
            buffer = buffer.replace("\n", "").rstrip(
                self._delimiters.segment_terminator
            )

            for segment in buffer.split(self._delimiters.segment_terminator):
                segment_fields = segment.split(self._delimiters.element_separator)
                yield (segment_fields[0].upper(), segment_fields)


class X12ModelReader:
    """
    Streams X12 Models from a X12 message or file
    """

    def __init__(self, x12_input: str):
        """
        Initializes the X12ModelReader with a x12_input.
        The x12 input may be a message payload or a path to a x12 file.

        :param x12_input: The X12 Message or a path to a X12 file
        """
        self._x12_segment_reader: X12SegmentReader = X12SegmentReader(x12_input)
        self._segment_lookup: Dict = SEGMENT_LOOKUP

    def __enter__(self):
        self._x12_segment_reader.__enter__()
        return self

    def _is_control_segment(self, segment_name) -> bool:
        """Returns True if a segment is a control segment"""
        return segment_name in (
            X12SegmentName.ISA,
            X12SegmentName.GS,
            X12SegmentName.GE,
            X12SegmentName.IEA,
        )

    def _is_transaction_header(self, segment_name) -> bool:
        """Returns True if a segment is a transaction header"""
        return segment_name == X12SegmentName.ST

    def model(self) -> Iterator[X12SegmentGroup]:
        """
        Creates a stream of X12 models from X12 segments
        """
        for segment_name, segment_fields in self._x12_segment_reader.segments():

            if self._is_control_segment(segment_name):
                continue

            if self._is_transaction_header(segment_name):

                transaction_code: str = segment_fields[1]
                implementation_version: str = segment_fields[3]

                parser: X12SegmentParser = X12SegmentParser.load_parser(
                    transaction_code, implementation_version
                )

            model: X12SegmentGroup = parser.parse(segment_name, segment_fields)
            if model:
                yield model

    def __exit__(self, exc_type, exc_val, exc_tb) -> NoReturn:
        """
        Exits the X12ModelReader and releases resources
        """
        self._x12_segment_reader.__exit__(exc_type, exc_val, exc_tb)
