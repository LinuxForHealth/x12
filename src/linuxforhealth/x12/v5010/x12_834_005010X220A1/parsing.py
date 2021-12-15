"""
parsing.py

Parses X12 Enrollment 834 005010X220A1 segments into a transactional domain model.

The parsing module includes a specific parser for the 270 transaction and loop parsing functions to create new loops
as segments are streamed to the transactional data model.

Loop parsing functions are implemented as set_[description]_loop(context: X12ParserContext, segment_data: Dict).
"""
from enum import Enum

from linuxforhealth.x12.parsing import match, X12ParserContext
from typing import Optional, Dict


class TransactionLoops(str, Enum):
    """
    The loops used to support the 270 005010X279A1 format.
    """

    HEADER = "header"
    FOOTER = "footer"


@match("ST")
def set_header_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the transaction set header loop for the 270 transaction set.

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment's data
    """

    context.transaction_data[TransactionLoops.HEADER] = {
        "dtp_segment": [],
        "qty_segment": []
    }

    context.set_loop_context(
        TransactionLoops.HEADER, context.transaction_data[TransactionLoops.HEADER]
    )


@match("SE")
def set_se_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the transaction set footer loop.

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment's data
    """

    context.set_loop_context(
        TransactionLoops.FOOTER, context.transaction_data["footer"]
    )
