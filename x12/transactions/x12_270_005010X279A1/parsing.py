"""
parsing.py

Parses X12 270 005010X279A1 segments into a transactional domain model.

The parsing module includes a specific parser for the 270 transaction and loop parsing functions to create new loops
as segments are streamed to the transactional data model.

Loop parsing functions are implemented as set_[description]_loop(context: X12ParserContext).
"""
from enum import Enum

from x12.parsing import match, X12ParserContext
from typing import Optional, Dict


class TransactionLoops(str, Enum):
    """
    The loops used to support the 270 005010X279A1 format.
    """

    HEADER = "header"
    INFORMATION_SOURCE = "loop_2000a"
    INFORMATION_SOURCE_NAME = "loop_2100a"
    INFORMATION_RECEIVER = "loop_2000b"
    INFORMATION_RECEIVER_NAME = "loop_2100b"
    SUBSCRIBER = "loop_2000c"
    SUBSCRIBER_NAME = "loop_2100c"
    SUBSCRIBER_ELIGIBILITY = "loop_2110c"
    DEPENDENT = "loop_2000d"
    DEPENDENT_NAME = "loop_2100d"
    DEPENDENT_ELIGIBILITY = "loop_2110d"
    FOOTER = "footer"


def _get_info_source(context) -> Dict:
    """Returns the current information source"""

    return context.transaction_data[TransactionLoops.INFORMATION_SOURCE][-1]


def _get_info_receiver(context) -> Dict:
    """Returns the current information receiver"""

    info_source = _get_info_source(context)
    return info_source[TransactionLoops.INFORMATION_RECEIVER][-1]


def _get_subscriber(context) -> Dict:
    """Returns the current subscriber"""
    info_receiver = _get_info_receiver(context)
    return info_receiver[TransactionLoops.SUBSCRIBER][-1]


# eligibility 270 loop parsing functions
@match("ST")
def set_header_loop(context: X12ParserContext) -> None:
    """
    Sets the transaction set header loop for the 270 transaction set.

    :param context: The X12Parsing context which contains the current loop and transaction record.
    """

    context.set_loop_context(
        TransactionLoops.HEADER, context.transaction_data[TransactionLoops.HEADER]
    )


@match("HL", conditions={"hierarchical_level_code": "20"})
def set_information_source_hl_loop(context: X12ParserContext) -> None:
    """
    Sets the Information Source (Payer/Clearinghouse) loop.

    :param context: The X12Parsing context which contains the current loop and transaction record.
    """

    if TransactionLoops.INFORMATION_SOURCE not in context.transaction_data:
        context.transaction_data[TransactionLoops.INFORMATION_SOURCE] = [{}]
    else:
        context.transaction_data[TransactionLoops.INFORMATION_SOURCE].append({})

    info_source = context.transaction_data[TransactionLoops.INFORMATION_SOURCE][-1]
    context.set_loop_context(TransactionLoops.INFORMATION_SOURCE, info_source)


@match("HL", conditions={"hierarchical_level_code": "21"})
def set_information_receiver_hl_loop(context: X12ParserContext) -> None:
    """
    Sets the Information Receiver (Provider) loop.

    :param context: The X12Parsing context which contains the current loop and transaction record.
    """

    info_source = _get_info_source(context)

    if TransactionLoops.INFORMATION_RECEIVER not in info_source:
        info_source[TransactionLoops.INFORMATION_RECEIVER] = [{}]
    else:
        info_source[TransactionLoops.INFORMATION_RECEIVER].append({})

    info_receiver = info_source[TransactionLoops.INFORMATION_RECEIVER][-1]
    context.set_loop_context(TransactionLoops.INFORMATION_RECEIVER, info_receiver)


@match("HL", conditions={"hierarchical_level_code": "22"})
def set_subscriber_hl_loop(context: X12ParserContext) -> None:
    """
    Sets the Subscriber (Member) loop
    Initializes optional TRN segment list.

    :param context: The X12Parsing context which contains the current loop and transaction record.
    """

    info_receiver = _get_info_receiver(context)

    if TransactionLoops.SUBSCRIBER not in info_receiver:
        info_receiver[TransactionLoops.SUBSCRIBER] = [{}]
    else:
        info_receiver[TransactionLoops.SUBSCRIBER].append({})

    subscriber = info_receiver[TransactionLoops.SUBSCRIBER][-1]
    subscriber["trn_segment"] = []

    context.set_loop_context(TransactionLoops.SUBSCRIBER, subscriber)


@match("NM1")
def set_entity_name_loop(context: X12ParserContext) -> None:
    """
    Sets the entity name loop based on the current loop context.
    Initializes optional REF segment list

    :param context: The X12Parsing context which contains the current loop and transaction record.
    """

    new_loop_name: Optional[str] = None

    if context.loop_name == TransactionLoops.INFORMATION_SOURCE:
        new_loop_name = TransactionLoops.INFORMATION_SOURCE_NAME
    elif context.loop_name == TransactionLoops.INFORMATION_RECEIVER:
        new_loop_name = TransactionLoops.INFORMATION_RECEIVER_NAME
    elif context.loop_name == TransactionLoops.SUBSCRIBER:
        new_loop_name = TransactionLoops.SUBSCRIBER_NAME
    elif context.loop_name == TransactionLoops.DEPENDENT:
        new_loop_name = TransactionLoops.DEPENDENT_NAME

    context.loop_container[new_loop_name] = {"ref_segment": []}
    context.set_loop_context(new_loop_name, context.loop_container[new_loop_name])


@match("EQ")
def set_eligibility_inquiry_loop(context: X12ParserContext) -> None:
    """
    Sets the eligibility inquiry loop, 2110C or 2110D, for a subscriber or dependent record.
    """

    new_loop_name: Optional[str] = None

    if context.loop_name == TransactionLoops.SUBSCRIBER_NAME:
        new_loop_name = TransactionLoops.SUBSCRIBER_ELIGIBILITY
    elif context.loop_name == TransactionLoops.DEPENDENT_NAME:
        new_loop_name = TransactionLoops.DEPENDENT_ELIGIBILITY

    context.loop_container[new_loop_name] = {"amt_segment": []}
    context.set_loop_context(new_loop_name, context.loop_container[new_loop_name])


@match("HL", conditions={"hierarchical_level_code": "23"})
def set_dependent_hl_loop(context: X12ParserContext) -> None:
    subscriber = _get_subscriber(context)

    if TransactionLoops.DEPENDENT not in subscriber:
        subscriber[TransactionLoops.DEPENDENT] = [{}]
    else:
        subscriber[TransactionLoops.DEPENDENT].append({})

    dependent = subscriber[TransactionLoops.DEPENDENT][-1]
    dependent["trn_segment"] = []

    context.set_loop_context(TransactionLoops.DEPENDENT, dependent)


@match("SE")
def set_se_loop(context: X12ParserContext) -> None:
    """
    Sets the transaction set footer loop.

    :param context: The X12Parsing context which contains the current loop and transaction record.
    """

    context.set_loop_context(
        TransactionLoops.FOOTER, context.transaction_data["footer"]
    )
