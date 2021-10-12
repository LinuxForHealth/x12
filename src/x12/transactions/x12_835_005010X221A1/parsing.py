"""
parsing.py

Parses X12 835 005010X221A1 segments into a transactional domain model.

The parsing module includes a specific parser for the 835 transaction and loop parsing functions to create new loops
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
    PAYER_IDENTIFICATION = "loop_1000a"
    FOOTER = "footer"


def _get_header(context: X12ParserContext) -> Dict:
    """Returns the 837 transaction header"""
    return context.transaction_data[TransactionLoops.HEADER]


@match("ST")
def set_header_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the transaction set header loop for the 835 transaction set.

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """

    context.set_loop_context(
        TransactionLoops.HEADER, context.transaction_data[TransactionLoops.HEADER]
    )


@match("N1", conditions={"entity_identifier_code": "PR"})
def set_payer_identification_loop(
    context: X12ParserContext, segment_data: Dict
) -> None:
    """
    Sets the payer identification loop

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    context.transaction_data[TransactionLoops.PAYER_IDENTIFICATION] = {
        "ref_segment": []
    }
    loop_data = context.transaction_data[TransactionLoops.PAYER_IDENTIFICATION]
    context.set_loop_context(TransactionLoops.PAYER_IDENTIFICATION, loop_data)


@match("SE")
def set_se_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the transaction set footer loop.

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """

    context.set_loop_context(
        TransactionLoops.FOOTER, context.transaction_data["footer"]
    )
