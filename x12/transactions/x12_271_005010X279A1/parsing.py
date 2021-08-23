"""
parsing.py

Parses X12 271 005010X279A1 segments into a transactional domain model.

The parsing module includes a specific parser for the 271 transaction and loop parsing functions to create new loops
as segments are streamed to the transactional data model.

Loop parsing functions are implemented as set_[description]_loop(context: X12ParserContext).
"""
from enum import Enum

from x12.parsing import match, X12ParserContext
from typing import Dict, Set


class TransactionLoops(str, Enum):
    """
    The loops used to support the 271 005010X279A1 format.
    """

    HEADER = "header"
    INFORMATION_SOURCE = "loop_2000a"
    INFORMATION_SOURCE_NAME = "loop_2100a"
    INFORMATION_RECEIVER = "loop_2000b"
    INFORMATION_RECEIVER_NAME = "loop_2100b"
    SUBSCRIBER = "loop_2000c"
    SUBSCRIBER_NAME = "loop_2100c"
    SUBSCRIBER_ELIGIBILITY = "loop_2110c"
    SUBSCRIBER_ADDITIONAL_ELIGIBILITY = "loop_2115c"
    SUBSCRIBER_RELATED_BENEFIT_NAME = "loop_2120c"
    DEPENDENT = "loop_2000d"
    DEPENDENT_NAME = "loop_2100d"
    DEPENDENT_ELIGIBILITY = "loop_2110d"
    DEPENDENT_ADDITIONAL_ELIGIBILITY = "loop_2115d"
    DEPENDENT_RELATED_BENEFIT_NAME = "loop_2120d"
    FOOTER = "footer"


SUBSCRIBER_LOOPS: Set[TransactionLoops] = {
    TransactionLoops.SUBSCRIBER,
    TransactionLoops.SUBSCRIBER_NAME,
    TransactionLoops.SUBSCRIBER_ELIGIBILITY,
    TransactionLoops.SUBSCRIBER_ADDITIONAL_ELIGIBILITY,
    TransactionLoops.SUBSCRIBER_RELATED_BENEFIT_NAME,
}

DEPENDENT_LOOPS: Set[TransactionLoops] = {
    TransactionLoops.DEPENDENT,
    TransactionLoops.DEPENDENT_NAME,
    TransactionLoops.DEPENDENT_ELIGIBILITY,
    TransactionLoops.DEPENDENT_ADDITIONAL_ELIGIBILITY,
    TransactionLoops.DEPENDENT_RELATED_BENEFIT_NAME,
}


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


def _get_dependent(context) -> Dict:
    """Returns the current dependent"""
    subscriber = _get_subscriber(context)
    return subscriber[TransactionLoops.DEPENDENT][-1]


def _get_subscriber_eligibility(context) -> Dict:
    """Returns the current subscriber eligibility"""
    subscriber = _get_subscriber(context)
    return subscriber[TransactionLoops.SUBSCRIBER_NAME][
        TransactionLoops.SUBSCRIBER_ELIGIBILITY
    ][-1]


def _get_dependent_eligibility(context) -> Dict:
    """Returns the current dependent eligibility"""
    dependent = _get_dependent(context)
    return dependent[TransactionLoops.DEPENDENT_NAME][
        TransactionLoops.DEPENDENT_ELIGIBILITY
    ][-1]


@match("ST")
def set_header_loop(context: X12ParserContext) -> None:
    """
    Sets the transaction set header loop.
    Creates initial data structures for the record

    :param context: The X12Parsing context which contains the current loop and transaction record.
    """
    context.transaction_data[TransactionLoops.HEADER] = {"bht_segment": None}

    context.set_loop_context(
        TransactionLoops.HEADER, context.transaction_data[TransactionLoops.HEADER]
    )


@match("HL", {"hierarchical_level_code": "20"})
def set_info_source_loop(context: X12ParserContext) -> None:
    """
    Sets the information source loop (Loop 2000A).

    :param context: The X12Parsing context which contains the current loop and transaction record.
    """
    info_source = {
        "hl_segment": None,
        "aaa_segment": [],
        "loop_2100a": None,
        "loop_2000b": [],
    }

    if TransactionLoops.INFORMATION_SOURCE not in context.transaction_data:
        context.transaction_data[TransactionLoops.INFORMATION_SOURCE] = []

    context.transaction_data[TransactionLoops.INFORMATION_SOURCE].append(info_source)
    current_record = context.transaction_data[TransactionLoops.INFORMATION_SOURCE][-1]
    context.set_loop_context(TransactionLoops.INFORMATION_SOURCE, current_record)


@match("NM1")
def set_info_source_name_loop(context: X12ParserContext) -> None:
    """
    Sets the information source name loop (Loop 2100A)

    :param context: The X12Parsing context which contains the current loop and transaction record.
    """
    if context.loop_name != TransactionLoops.INFORMATION_SOURCE:
        return

    info_source_name = {"nm1_segment": None, "per_segment": [], "aaa_segment": []}

    info_source = _get_info_source(context)
    info_source[TransactionLoops.INFORMATION_SOURCE_NAME] = info_source_name
    context.set_loop_context(TransactionLoops.INFORMATION_SOURCE_NAME, info_source_name)


@match("HL", {"hierarchical_level_code": "21"})
def set_info_receiver_loop(context: X12ParserContext) -> None:
    """
    Sets the information receiver loop (Loop 2000B)

    :param context: The X12Parsing context which contains the current loop and transaction record.
    """
    info_source = _get_info_source(context)

    info_source[TransactionLoops.INFORMATION_RECEIVER].append(
        {"hl_segment": None, "loop_2100b": None, "loop_2000c": []}
    )

    info_receiver = info_source[TransactionLoops.INFORMATION_RECEIVER][-1]
    context.set_loop_context(TransactionLoops.INFORMATION_RECEIVER, info_receiver)


@match("NM1")
def set_info_receiver_name_loop(context: X12ParserContext) -> None:
    """
    Sets the information receiver name loop (Loop 2100B)

    :param context: The X12Parsing context which contains the current loop and transaction record.
    """
    if context.loop_name != TransactionLoops.INFORMATION_RECEIVER:
        return

    info_receiver = _get_info_receiver(context)
    info_receiver[TransactionLoops.INFORMATION_RECEIVER_NAME] = {
        "nm1_segment": None,
        "ref_segment": [],
        "n3_segment": None,
        "n4_segment": None,
        "aaa_segment": None,
        "prv_segment": None,
    }

    info_receiver_name = info_receiver[TransactionLoops.INFORMATION_RECEIVER_NAME]
    context.set_loop_context(
        TransactionLoops.INFORMATION_RECEIVER_NAME, info_receiver_name
    )


@match("HL", {"hierarchical_level_code": "22"})
def set_subscriber_loop(context: X12ParserContext) -> None:
    """
    Sets the subscriber loop (Loop 2000C)

    :param context: The X12Parsing context which contains the current loop and transaction record.
    """
    info_receiver = _get_info_receiver(context)

    info_receiver[TransactionLoops.SUBSCRIBER].append(
        {"hl_segment": None, "trn_segment": [], "loop_2100c": None, "loop_2000d": []}
    )

    subscriber = info_receiver[TransactionLoops.SUBSCRIBER][-1]
    context.set_loop_context(TransactionLoops.SUBSCRIBER, subscriber)


@match("HL", {"hierarchical_level_code": "23"})
def set_dependent_loop(context: X12ParserContext) -> None:
    """
    Sets the dependent loop (Loop 2000D)

    :param context: The X12Parsing context which contains the current loop and transaction record.
    """
    subscriber = _get_subscriber(context)

    subscriber[TransactionLoops.DEPENDENT].append(
        {
            "hl_segment": None,
            "trn_segment": [],
            "loop_2100d": None,
        }
    )

    dependent = subscriber[TransactionLoops.DEPENDENT][-1]
    context.set_loop_context(TransactionLoops.DEPENDENT, dependent)


@match("NM1")
def set_member_name_loop(context: X12ParserContext) -> None:
    """
    Sets the subscriber or dependent name loop (Loop 2100C or 2100D)

    :param context: The X12Parsing context which contains the current loop and transaction record.
    """
    if context.loop_name not in (
        TransactionLoops.SUBSCRIBER,
        TransactionLoops.DEPENDENT,
    ):
        return

    if context.loop_name == TransactionLoops.SUBSCRIBER:
        member = _get_subscriber(context)
        loop_name = TransactionLoops.SUBSCRIBER_NAME
        eligibility_loop = TransactionLoops.SUBSCRIBER_ELIGIBILITY
    else:
        member = _get_dependent(context)
        loop_name = TransactionLoops.DEPENDENT_NAME
        eligibility_loop = TransactionLoops.DEPENDENT_ELIGIBILITY

    member[loop_name] = {
        "nm1_segment": None,
        "ref_segment": [],
        "n3_segment": None,
        "n4_segment": None,
        "aaa_segment": [],
        "prv_segment": None,
        "dmg_segment": None,
        "ins_segment": None,
        "hi_segment": None,
        "dtp_segment": [],
        "mpi_segment": None,
        eligibility_loop: [],
    }

    context.set_loop_context(loop_name, member[loop_name])


@match("EB")
def set_member_eligibility_benefit_info_loop(context: X12ParserContext) -> None:
    """
    Sets the subscriber or dependent eligibility/benefit info loop (Loop 2110C/2110D)

    :param context: The X12Parsing context which contains the current loop and transaction record.
    """
    if context.loop_name not in (
        TransactionLoops.SUBSCRIBER_NAME,
        TransactionLoops.SUBSCRIBER_ELIGIBILITY,
        TransactionLoops.DEPENDENT_NAME,
        TransactionLoops.DEPENDENT_ELIGIBILITY,
    ):
        return

    if context.loop_name in SUBSCRIBER_LOOPS:
        member = _get_subscriber(context)
        record = member[TransactionLoops.SUBSCRIBER_NAME][
            TransactionLoops.SUBSCRIBER_ELIGIBILITY
        ]
        eligibility_loop = TransactionLoops.SUBSCRIBER_ELIGIBILITY
        additional_info_loop = TransactionLoops.SUBSCRIBER_ADDITIONAL_ELIGIBILITY
        benefit_entity_loop = TransactionLoops.SUBSCRIBER_RELATED_BENEFIT_NAME
    else:
        member = _get_dependent(context)
        record = member[TransactionLoops.DEPENDENT_NAME][
            TransactionLoops.DEPENDENT_ELIGIBILITY
        ]
        eligibility_loop = TransactionLoops.DEPENDENT_ELIGIBILITY
        additional_info_loop = TransactionLoops.DEPENDENT_ADDITIONAL_ELIGIBILITY
        benefit_entity_loop = TransactionLoops.DEPENDENT_RELATED_BENEFIT_NAME

    record.append(
        {
            "eb_segment": None,
            "hsd_segment": [],
            "ref_segment": [],
            "dtp_segment": [],
            "aaa_segment": [],
            "msg_segment": [],
            additional_info_loop: [],
            "ls_segment": None,
            benefit_entity_loop: [],
            "le_segment": None,
        }
    )

    member_eligibility = record[-1]
    context.set_loop_context(eligibility_loop, member_eligibility)


@match("III")
def set_member_additional_information(context: X12ParserContext) -> None:
    """
    Sets the subscriber/dependent eligibility benefit additional information loop (Loop 2115c/2115d)

    :param context: The X12Parsing context which contains the current loop and transaction record.
    """
    if context.loop_name in SUBSCRIBER_LOOPS:
        eligibility = _get_subscriber_eligibility(context)
        loop_name = TransactionLoops.SUBSCRIBER_ADDITIONAL_ELIGIBILITY
    else:
        eligibility = _get_dependent_eligibility(context)
        loop_name = TransactionLoops.DEPENDENT_ADDITIONAL_ELIGIBILITY

    eligibility[loop_name].append({"iii_segment": None})

    additional_info = eligibility[loop_name][-1]
    context.set_loop_context(loop_name, additional_info)


@match("LS")
def set_loop_header_in_eligibility_loop(context: X12ParserContext) -> None:
    """
    Ensures that the Loop Header Segment is written to the Member (Subscriber or Dependent)

    :param context: The X12Parsing context which contains the current loop and transaction record.
    """
    if context.loop_name in SUBSCRIBER_LOOPS:
        related_benefit = TransactionLoops.SUBSCRIBER_RELATED_BENEFIT_NAME
        loop_name = TransactionLoops.SUBSCRIBER_ELIGIBILITY
        eligibility_record = _get_subscriber_eligibility(context)
    else:
        related_benefit = TransactionLoops.DEPENDENT_RELATED_BENEFIT_NAME
        loop_name = TransactionLoops.DEPENDENT_ELIGIBILITY
        eligibility_record = _get_dependent_eligibility(context)

    eligibility_record[related_benefit].append(
        {
            "nm1_segment": None,
            "n3_segment": None,
            "n4_segment": None,
            "per_segment": [],
            "prv_segment": None,
        }
    )

    context.set_loop_context(loop_name, eligibility_record)


@match("NM1")
def set_benefit_related_entity_name_loop(context: X12ParserContext) -> None:
    """
    Creates the structure for the Benefit Related Entity Name Loop.
    The Benefit Related Entity Name Loop is entered either through the Eligibility or Additional Eligibility Loop.

    :param context: The X12Parsing context which contains the current loop and transaction record.
    """
    if context.loop_name not in (
        TransactionLoops.SUBSCRIBER_ELIGIBILITY,
        TransactionLoops.SUBSCRIBER_ADDITIONAL_ELIGIBILITY,
        TransactionLoops.DEPENDENT_ELIGIBILITY,
        TransactionLoops.DEPENDENT_ADDITIONAL_ELIGIBILITY,
    ):
        return

    if context.loop_name in SUBSCRIBER_LOOPS:
        eligibility = _get_subscriber_eligibility(context)
        loop_name = TransactionLoops.SUBSCRIBER_RELATED_BENEFIT_NAME
    else:
        eligibility = _get_dependent_eligibility(context)
        loop_name = TransactionLoops.DEPENDENT_RELATED_BENEFIT_NAME

    related_entity = eligibility[loop_name][-1]
    context.set_loop_context(loop_name, related_entity)


@match("LE")
def set_loop_footer_in_eligibility_loop(context: X12ParserContext) -> None:
    """
    Ensures that the Loop Header Segment is written to the Member (Subscriber or Dependent)

    :param context: The X12Parsing context which contains the current loop and transaction record.
    """
    if context.loop_name in SUBSCRIBER_LOOPS:
        eligibility = _get_subscriber_eligibility(context)
        context.set_loop_context(TransactionLoops.SUBSCRIBER_ELIGIBILITY, eligibility)
    else:
        eligibility = _get_dependent_eligibility(context)
        context.set_loop_context(TransactionLoops.DEPENDENT_ELIGIBILITY, eligibility)


@match("SE")
def set_se_loop(context: X12ParserContext) -> None:
    """
    Sets the transaction set footer loop.

    :param context: The X12Parsing context which contains the current loop and transaction record.
    """

    context.set_loop_context(
        TransactionLoops.FOOTER, context.transaction_data["footer"]
    )
