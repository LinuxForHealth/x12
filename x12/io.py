"""
io.py

Supports X12 I/O operations such as reading, writing, and modeling raw models.
"""
from io import TextIOBase, StringIO
from x12.config import get_config, IsaDelimiters, X12VersionFields
from x12.support import is_x12_data, is_x12_file
from typing import Optional, Iterator, List, Tuple, NoReturn
from x12.models import X12Delimiters, X12VersionIdentifiers, X12ReaderContext


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

        self.x12_input: str = x12_input
        self.context: X12ReaderContext = X12ReaderContext.construct()
        self.context.delimiters = X12Delimiters.construct()
        self.context.version = X12VersionIdentifiers.construct()

        # set in __enter__
        self.buffer_size: Optional[int] = None
        self.x12_stream: Optional[TextIOBase] = None

    def _parse_isa_segment(self) -> NoReturn:
        """
        Parses fields from the ISA segment to set delimiters/instance attributes.
        The ISA segment is conveyed in the first 106 characters of the transmission.
        """
        self.x12_stream.seek(0)

        isa_segment: str = self.x12_stream.read(IsaDelimiters.SEGMENT_LENGTH)
        self.context.delimiters.element_separator = isa_segment[IsaDelimiters.ELEMENT_SEPARATOR]
        self.context.delimiters.repetition_separator = isa_segment[IsaDelimiters.REPETITION_SEPARATOR]
        self.context.delimiters.segment_terminator = isa_segment[IsaDelimiters.SEGMENT_TERMINATOR]
        self.context.delimiters.component_separator = isa_segment[IsaDelimiters.COMPONENT_SEPARATOR]

    def __enter__(self) -> "X12SegmentReader":
        """
        Initializes the X12 Stream and parses messages delimiters from the ISA segment.
        :return: The X12SegmentReader instance
        :raise: ValueError if the x12 input is invalid
        """
        if is_x12_file(self.x12_input):
            self.x12_stream = open(self.x12_input, "r")
        elif is_x12_data(self.x12_input):
            self.x12_stream = StringIO(self.x12_input)
        else:
            raise ValueError(
                "Invalid x12_input. Expecting X12 Message or valid path to X12 File"
            )

        self.buffer_size: int = get_config().x12_reader_buffer_size

        self.x12_stream.seek(0)
        if not self.x12_stream.read(IsaDelimiters.SEGMENT_LENGTH):
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
        if not self.x12_stream.closed:
            self.x12_stream.close()

        self.context = None
        self.x12_input = None
        self.x12_config = None

    def _is_control_segment(self, segment_name) -> bool:
        """returns True if the segment_name is a control segment"""
        return segment_name.upper() in ("ISA", "GS", "ST", "SE", "GE", "IEA")

    def _update_context(self, segment_fields) -> NoReturn:
        """
        Updates the current context attributes based on the current segment fields
        :param segment_fields: List of segment fields.
        """
        segment_name = segment_fields[0].upper()
        self.context.current_segment_name = segment_name
        self.context.current_segment = segment_fields

        if segment_name == "ISA":
            self.context.interchange_header = segment_fields
            self.context.version.interchange_control_version = segment_fields[X12VersionFields.ISA_CONTROL_VERSION]
        elif segment_name == "GS":
            self.context.functional_group_header = segment_fields
            self.context.version.functional_id_code = segment_fields[X12VersionFields.GS_FUNCTIONAL_CODE]
            self.context.version.functional_version_code = segment_fields[X12VersionFields.GS_FUNCTIONAL_VERSION]
        elif segment_name == "ST":
            self.context.transaction_set_header = segment_fields
            self.context.version.transaction_set_code = segment_fields[X12VersionFields.ST_TRANSACTION_CODE]

        if segment_name not in ("ISA", "GS", "GE", "IEA"):
            transaction_control_id = self.context.transaction_set_header[X12VersionFields.ST_TRANSACTION_CONTROL]
            self.context.segment_count[transaction_control_id] += 1

    def segments(self) -> Iterator[Tuple[str, List[str], X12ReaderContext]]:
        """
        Iterator function used to return X12 models from the underlying X12 stream.
        The read buffer size may be configured using X12_READER_BUFFER_SIZE.
        :return: Iterator containing segment name, segment fields, and the current context
        """
        self.x12_stream.seek(0)
        while True:
            buffer: str = self.x12_stream.read(self.buffer_size)

            if not buffer:
                break

            while buffer[-1] != self.context.delimiters.segment_terminator:
                next_character: str = self.x12_stream.read(1)
                if not next_character:
                    break
                buffer += next_character

            # buffer cleanup
            buffer = buffer.replace("\n", "").rstrip(
                self.context.delimiters.segment_terminator
            )

            for segment in buffer.split(self.context.delimiters.segment_terminator):
                segment_fields = segment.split(
                    self.context.delimiters.element_separator
                )
                self._update_context(segment_fields)
                yield (
                    self.context.current_segment_name,
                    self.context.current_segment,
                    self.context,
                )
