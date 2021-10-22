"""
parsing.py

Parses X12 276 005010X212 segments into a transactional domain model.

The parsing module includes a specific parser for the 276 transaction and loop parsing functions to create new loops
as segments are streamed to the transactional data model.

Loop parsing functions are implemented as set_[description]_loop(context: X12ParserContext, segment_data: Dict).
"""
from enum import Enum
from x12.parsing import X12ParserContext, match
from typing import Dict


class TransactionLoops(str, Enum):
    """
    The loops used to support the 835 005010X221A1 format.
    """

    HEADER = "header"
    FOOTER = "footer"


@match("ST")
def set_header_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the transaction set header loop for the 276 transaction set.

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """

    context.set_loop_context(
        TransactionLoops.HEADER, context.transaction_data[TransactionLoops.HEADER]
    )


@match("SE")
def set_footer_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the transaction set footer loop.

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """

    context.set_loop_context(
        TransactionLoops.FOOTER, context.transaction_data["footer"]
    )
