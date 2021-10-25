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
    INFORMATION_SOURCE_LEVEL = "loop_2000a"
    PAYER_NAME = "loop_2100a"
    INFORMATION_RECEIVER_LEVEL = "loop_2000b"
    INFORMATION_RECEIVER_NAME = "loop_2100b"
    SERVICE_PROVIDER_LEVEL = "loop_2000c"
    SERVICE_PROVIDER_NAME = "loop_2100c"
    SUBSCRIBER_LEVEL = "loop_2000d"
    SUBSCRIBER_NAME = "loop_2100d"
    SUBSCRIBER_CLAIM_STATUS_TRACKING_NUMBER = "loop_2200d"
    SUBSCRIBER_SERVICE_LINE_INFORMATION = "loop_2210d"
    DEPENDENT_LEVEL = "loop_2000e"
    DEPENDENT_NAME = "loop_2100e"
    DEPENDENT_CLAIM_STATUS_TRACKING_NUMBER = "loop_2200e"
    DEPENDENT_SERVICE_LINE_INFORMATION = "loop_2210e"
    FOOTER = "footer"


def _get_information_source(context: X12ParserContext) -> Dict:
    """Returns the current information source record"""
    return context.transaction_data[TransactionLoops.INFORMATION_SOURCE_LEVEL][-1]


def _get_information_receiver(context: X12ParserContext) -> Dict:
    """Returns the current information receiver record"""
    information_source = _get_information_source(context)
    return information_source[TransactionLoops.INFORMATION_RECEIVER_LEVEL][-1]


def _get_service_provider(context: X12ParserContext) -> Dict:
    """Returns the current service provider record"""
    information_receiver = _get_information_receiver(context)
    return information_receiver[TransactionLoops.SERVICE_PROVIDER_LEVEL][-1]


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


@match("HL", {"hierarchical_level_code": "20"})
def set_information_source_loop(context: X12ParserContext, segment_data: Dict):
    """
    Sets the information source loop

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    if TransactionLoops.INFORMATION_SOURCE_LEVEL not in context.transaction_data:
        context.transaction_data[TransactionLoops.INFORMATION_SOURCE_LEVEL] = []

    context.transaction_data[TransactionLoops.INFORMATION_SOURCE_LEVEL].append({})
    loop_record = context.transaction_data[TransactionLoops.INFORMATION_SOURCE_LEVEL][
        -1
    ]
    context.set_loop_context(TransactionLoops.INFORMATION_SOURCE_LEVEL, loop_record)


@match("NM1", {"entity_identifier_code": "PR"})
def set_payer_name_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the Information Source/Payer Name Loop

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    if context.loop_name == TransactionLoops.INFORMATION_SOURCE_LEVEL:
        information_source = _get_information_source(context)
        information_source[TransactionLoops.PAYER_NAME] = {}
        loop_record = information_source[TransactionLoops.PAYER_NAME]
        context.set_loop_context(TransactionLoops.PAYER_NAME, loop_record)


@match("HL", {"hierarchical_level_code": "21"})
def set_information_receiver_loop(
    context: X12ParserContext, segment_data: Dict
) -> None:
    """
    Sets the information receiver loop

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    information_source = _get_information_source(context)
    if TransactionLoops.INFORMATION_RECEIVER_LEVEL not in information_source:
        information_source[TransactionLoops.INFORMATION_RECEIVER_LEVEL] = []

    information_source[TransactionLoops.INFORMATION_RECEIVER_LEVEL].append({})
    loop_record = information_source[TransactionLoops.INFORMATION_RECEIVER_LEVEL][-1]
    context.set_loop_context(TransactionLoops.INFORMATION_RECEIVER_LEVEL, loop_record)


@match("NM1", {"entity_identifier_code": "41"})
def set_information_receiver_name_loop(
    context: X12ParserContext, segment_data: Dict
) -> None:
    """
    Sets the Information Receiver Name Loop

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    if context.loop_name == TransactionLoops.INFORMATION_RECEIVER_LEVEL:
        information_receiver = _get_information_receiver(context)
        information_receiver[TransactionLoops.INFORMATION_RECEIVER_NAME] = {}
        loop_record = information_receiver[TransactionLoops.INFORMATION_RECEIVER_NAME]
        context.set_loop_context(
            TransactionLoops.INFORMATION_RECEIVER_NAME, loop_record
        )


@match("HL", {"hierarchical_level_code": "19"})
def set_service_provider_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the service provider loop

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    information_receiver = _get_information_receiver(context)
    if TransactionLoops.SERVICE_PROVIDER_LEVEL not in information_receiver:
        information_receiver[TransactionLoops.SERVICE_PROVIDER_LEVEL] = []

    information_receiver[TransactionLoops.SERVICE_PROVIDER_LEVEL].append({})
    loop_record = information_receiver[TransactionLoops.SERVICE_PROVIDER_LEVEL][-1]
    context.set_loop_context(TransactionLoops.SERVICE_PROVIDER_LEVEL, loop_record)


@match("NM1", {"entity_identifier_code": "1P"})
def set_service_provider_name_loop(
    context: X12ParserContext, segment_data: Dict
) -> None:
    """
    Sets the Service Provider Name Loop

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    if context.loop_name == TransactionLoops.SERVICE_PROVIDER_LEVEL:
        service_provider = _get_service_provider(context)
        service_provider[TransactionLoops.SERVICE_PROVIDER_NAME] = {}
        loop_record = service_provider[TransactionLoops.SERVICE_PROVIDER_NAME]
        context.set_loop_context(TransactionLoops.SERVICE_PROVIDER_NAME, loop_record)


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
