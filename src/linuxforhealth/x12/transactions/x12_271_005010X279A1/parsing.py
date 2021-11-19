"""
parsing.py

Parses X12 271 005010X279A1 segments into a transactional domain model.

The parsing module includes a specific parser for the 271 transaction and loop parsing functions to create new loops
as segments are streamed to the transactional data model.

Loop parsing functions are implemented as set_[description]_loop(context: X12ParserContext, segment_data: Dict).
"""
from enum import Enum

from linuxforhealth.x12.parsing import match, X12ParserContext
from typing import Dict


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


# Subscriber HL Segment Hierarchy Level Code
SUBSCRIBER_HIERARCHY_LEVEL = "22"


def _get_info_source(context) -> Dict:
    """Returns the current information source"""
    return context.transaction_data[TransactionLoops.INFORMATION_SOURCE][-1]


def _get_info_receiver(context) -> Dict:
    """Returns the current information receiver"""
    info_source = _get_info_source(context)
    return info_source[TransactionLoops.INFORMATION_RECEIVER][-1]


def _is_subscriber_patient(context) -> bool:
    """Returns true if the current context contains a subscriber that is the patient"""
    hl_level_code = context.hl_segment.get("hierarchical_level_code")
    hl_child_code = context.hl_segment.get("hierarchical_child_code")
    return hl_level_code == SUBSCRIBER_HIERARCHY_LEVEL and hl_child_code == "0"


def _get_eligibility(context) -> Dict:
    """Returns the current eligibility record"""
    if _is_subscriber_patient(context):
        name_loop = TransactionLoops.SUBSCRIBER_NAME
        eligibility_loop = TransactionLoops.SUBSCRIBER_ELIGIBILITY
    else:
        name_loop = TransactionLoops.DEPENDENT_NAME
        eligibility_loop = TransactionLoops.DEPENDENT_ELIGIBILITY

    return context.patient_record[name_loop][eligibility_loop][-1]


@match("ST")
def set_header_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the transaction set header loop.
    Creates initial data structures for the record

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment's data
    """
    context.transaction_data[TransactionLoops.HEADER] = {}
    context.set_loop_context(
        TransactionLoops.HEADER, context.transaction_data[TransactionLoops.HEADER]
    )


@match("HL", {"hierarchical_level_code": "20"})
def set_information_source_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the information source loop (Loop 2000A)

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment's data
    """
    if TransactionLoops.INFORMATION_SOURCE not in context.transaction_data:
        context.transaction_data[TransactionLoops.INFORMATION_SOURCE] = []

    context.transaction_data[TransactionLoops.INFORMATION_SOURCE].append(
        {"aaa_segment": []}
    )
    information_source = context.transaction_data[TransactionLoops.INFORMATION_SOURCE][
        -1
    ]
    context.set_loop_context(TransactionLoops.INFORMATION_SOURCE, information_source)


@match("NM1")
def set_information_source_name_loop(
    context: X12ParserContext, segment_data: Dict
) -> None:
    """
    Sets the information source name (Loop 2100A)

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment's data
    """
    if context.loop_name == TransactionLoops.INFORMATION_SOURCE:
        context.loop_container[TransactionLoops.INFORMATION_SOURCE_NAME] = {
            "per_segment": [],
            "aaa_segment": [],
        }
        context.set_loop_context(
            TransactionLoops.INFORMATION_SOURCE_NAME,
            context.loop_container[TransactionLoops.INFORMATION_SOURCE_NAME],
        )


@match("HL", {"hierarchical_level_code": "21"})
def set_information_receiver_loop(
    context: X12ParserContext, segment_data: Dict
) -> None:
    """
    Sets the information receiver loop (Loop 2000B)

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment's data
    """
    info_source = _get_info_source(context)

    if TransactionLoops.INFORMATION_RECEIVER not in info_source:
        info_source[TransactionLoops.INFORMATION_RECEIVER] = []

    info_source[TransactionLoops.INFORMATION_RECEIVER].append({})
    info_receiver = info_source[TransactionLoops.INFORMATION_RECEIVER][-1]
    context.set_loop_context(TransactionLoops.INFORMATION_RECEIVER, info_receiver)


@match("NM1")
def set_information_receiver_name_loop(
    context: X12ParserContext, segment_data: Dict
) -> None:
    """
    Sets the information receiver name (Loop 2100B)

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment's data
    """
    if context.loop_name == TransactionLoops.INFORMATION_RECEIVER:
        context.loop_container[TransactionLoops.INFORMATION_RECEIVER_NAME] = {
            "ref_segment": [],
            "aaa_segment": [],
        }
        context.set_loop_context(
            TransactionLoops.INFORMATION_RECEIVER_NAME,
            context.loop_container[TransactionLoops.INFORMATION_RECEIVER_NAME],
        )


@match("HL", {"hierarchical_level_code": "22"})
def set_subscriber_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the subscriber loop (Loop 2000C)

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment's data
    """
    info_receiver = _get_info_receiver(context)

    if TransactionLoops.SUBSCRIBER not in info_receiver:
        info_receiver[TransactionLoops.SUBSCRIBER] = []

    info_receiver[TransactionLoops.SUBSCRIBER].append({"trn_segment": []})
    context.subscriber_record = info_receiver[TransactionLoops.SUBSCRIBER][-1]
    context.set_loop_context(TransactionLoops.SUBSCRIBER, context.subscriber_record)

    if _is_subscriber_patient(context):
        context.patient_record = context.subscriber_record


@match("NM1", conditions={"entity_identifier_code": "IL"})
def set_subscriber_name_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the subscriber loop (Loop 2100C)

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment's data
    """
    if context.loop_name == TransactionLoops.SUBSCRIBER:
        context.subscriber_record[TransactionLoops.SUBSCRIBER_NAME] = {
            "ref_segment": [],
            "aaa_segment": [],
            "dtp_segment": [],
        }
        context.set_loop_context(
            TransactionLoops.SUBSCRIBER_NAME,
            context.subscriber_record[TransactionLoops.SUBSCRIBER_NAME],
        )


@match("EB")
def set_eligibility_benefit_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the eligibility benefit loop for subscriber (2110C) or dependents (2110D)
    """
    if _is_subscriber_patient(context):
        name_loop = TransactionLoops.SUBSCRIBER_NAME
        eligibility_loop = TransactionLoops.SUBSCRIBER_ELIGIBILITY
    else:
        name_loop = TransactionLoops.DEPENDENT_NAME
        eligibility_loop = TransactionLoops.DEPENDENT_ELIGIBILITY

    if eligibility_loop not in context.patient_record[name_loop]:
        context.patient_record[name_loop][eligibility_loop] = []

    context.patient_record[name_loop][eligibility_loop].append(
        {
            "hsd_segment": [],
            "ref_segment": [],
            "dtp_segment": [],
            "aaa_segment": [],
            "msg_segment": [],
        }
    )
    eligibility_record = context.patient_record[name_loop][eligibility_loop][-1]
    context.set_loop_context(eligibility_loop, eligibility_record)


@match("III")
def set_additional_benefit_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the additional benefit information loop - subscriber (Loop 2115C), dependent (Loop 2115D)

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment's data
    """
    if _is_subscriber_patient(context):
        additional_benefit_loop = TransactionLoops.SUBSCRIBER_ADDITIONAL_ELIGIBILITY
    else:
        additional_benefit_loop = TransactionLoops.DEPENDENT_ADDITIONAL_ELIGIBILITY

    eligibility = _get_eligibility(context)

    if additional_benefit_loop not in eligibility:
        eligibility[additional_benefit_loop] = []

    eligibility[additional_benefit_loop].append({})
    additional_benefit = eligibility[additional_benefit_loop][-1]
    context.set_loop_context(additional_benefit_loop, additional_benefit)


@match("LS")
def set_loop_header_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Resets the loop context to the Eligibility Loop 2120C/D (Subscriber and Dependent)
    The LS segment precedes the Subscriber/Dependent Benefit Related Entity Name

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment's data
    """
    eligibility = _get_eligibility(context)

    if _is_subscriber_patient(context):
        loop_name = TransactionLoops.SUBSCRIBER_ELIGIBILITY
    else:
        loop_name = TransactionLoops.DEPENDENT_ELIGIBILITY

    context.set_loop_context(loop_name, eligibility)


@match("NM1")
def set_benefit_related_entity_loop(
    context: X12ParserContext, segment_data: Dict
) -> None:
    """
    Supports the Benefit Related Entity Name Loop for the Subscriber (2120C) and Dependent (2120D).

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment's data
    """
    if context.loop_name not in (
        TransactionLoops.DEPENDENT_ELIGIBILITY,
        TransactionLoops.SUBSCRIBER_ELIGIBILITY,
    ):
        return

    if _is_subscriber_patient(context):
        benefit_related_entity_loop = TransactionLoops.SUBSCRIBER_RELATED_BENEFIT_NAME
    else:
        benefit_related_entity_loop = TransactionLoops.DEPENDENT_RELATED_BENEFIT_NAME

    eligibility = _get_eligibility(context)

    if benefit_related_entity_loop not in eligibility:
        eligibility[benefit_related_entity_loop] = []

    eligibility[benefit_related_entity_loop].append(
        {
            "per_segment": [],
        }
    )

    benefit_related_entity = eligibility[benefit_related_entity_loop][-1]
    context.set_loop_context(benefit_related_entity_loop, benefit_related_entity)


@match("LE")
def set_loop_footer_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Ensures that the Loop Footer Segment is written to the Member (Subscriber or Dependent)
    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment's data
    """
    eligibility = _get_eligibility(context)

    if _is_subscriber_patient(context):
        context.set_loop_context(TransactionLoops.SUBSCRIBER_ELIGIBILITY, eligibility)
    else:
        context.set_loop_context(TransactionLoops.DEPENDENT_ELIGIBILITY, eligibility)


@match("HL", {"hierarchical_level_code": "23"})
def set_dependent_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the dependent loop (Loop 2000D)

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment's data
    """
    if TransactionLoops.DEPENDENT not in context.subscriber_record:
        context.subscriber_record[TransactionLoops.DEPENDENT] = []

    context.subscriber_record[TransactionLoops.DEPENDENT].append({"trn_segment": []})
    context.patient_record = context.subscriber_record[TransactionLoops.DEPENDENT][-1]
    context.set_loop_context(TransactionLoops.DEPENDENT, context.patient_record)


@match("NM1", conditions={"entity_identifier_code": "03"})
def set_dependent_name_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the dependent name loop (Loop 2100D)

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment's data
    """
    if context.loop_name == TransactionLoops.DEPENDENT:
        context.patient_record[TransactionLoops.DEPENDENT_NAME] = {
            "ref_segment": [],
            "aaa_segment": [],
            "dtp_segment": [],
        }
        context.set_loop_context(
            TransactionLoops.DEPENDENT_NAME,
            context.patient_record[TransactionLoops.DEPENDENT_NAME],
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
