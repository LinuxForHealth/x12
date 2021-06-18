"""
io.py

Supports X12 I/O operations such as reading, writing, and modeling raw models.
"""
from io import TextIOBase, StringIO
from x12.config import get_config, X12Config
from x12.support import is_x12_data, is_x12_file
from typing import Union, Iterator, List
from x12.models import X12Delimiters


class X12SegmentReader:
    """
    Streams models from a X12 message or file.

    with X12Reader(x12_data) as r:
       for segment in r.models():
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

        # set in __enter__
        self.buffer_size: Union[None, int] = None
        self.x12_stream: Union[None, TextIOBase] = None
        self.x12_delimiters: Union[None, X12Delimiters] = None
        self.interchange_version: Union[None, str] = None

    def _parse_isa_segment(self, x12_config: X12Config):
        """
        Parses fields from the ISA segment to set delimiters/instance attributes.
        The ISA segment is conveyed in the first 106 characters of the transmission.
        """
        self.x12_stream.seek(0)

        isa_segment: str = self.x12_stream.read(x12_config.x12_isa_segment_length)
        isa_tokens = isa_segment[0:105].split("*")

        self.x12_delimiters = X12Delimiters(
            element_separator=isa_segment[x12_config.x12_isa_element_separator],
            repetition_separator=isa_tokens[11],
            segment_terminator=isa_segment[-1],
            component_separator=isa_tokens[16],
        )
        self.interchange_version = isa_tokens[12]

    def __enter__(self) -> "X12SegmentReader":
        """
        Initializes the X12 Stream and parses message delimiters
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

        x12_config = get_config()
        self.buffer_size: int = x12_config.x12_reader_buffer_size

        self.x12_stream.seek(0)
        if not self.x12_stream.read(x12_config.x12_isa_segment_length):
            raise ValueError("Invalid X12Stream")

        self._parse_isa_segment(x12_config)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Closes the X12SegmentReader's X12 Stream
        :param exc_type: Exception Type
        :param exc_val: Exception Value
        :param exc_tb: Exception traceback
        """
        if not self.x12_stream.closed:
            self.x12_stream.close()

    def segments(self) -> Iterator[List[str]]:
        """
        Iterator function used to return X12 models from the underlying X12 stream.
        The read buffer size may be configured using X12_READER_BUFFER_SIZE.
        :return: X12 Segment
        """
        self.x12_stream.seek(0)
        while True:
            buffer: str = self.x12_stream.read(self.buffer_size)

            if not buffer:
                break

            while buffer[-1] != self.x12_delimiters.segment_terminator:
                next_character: str = self.x12_stream.read(1)
                if not next_character:
                    break
                buffer += next_character

            # use rstrip to remove trailing empty strings
            for segment in buffer.rstrip(self.x12_delimiters.segment_terminator).split(
                self.x12_delimiters.segment_terminator
            ):
                yield segment
