"""
parsing.py

Parses X12 276 005010X212 segments into a transactional domain model.

The parsing module includes a specific parser for the 276 transaction and loop parsing functions to create new loops
as segments are streamed to the transactional data model.

Loop parsing functions are implemented as set_[description]_loop(context: X12ParserContext, segment_data: Dict).
"""
from enum import Enum
from linuxforhealth.x12.parsing import X12ParserContext, match
from typing import Dict, Optional


class TransactionLoops(str, Enum):
    """
    The loops used to support the 276 005010X212 format.
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


def _get_information_source(context: X12ParserContext) -> Optional[Dict]:
    return context.transaction_data[TransactionLoops.INFORMATION_SOURCE_LEVEL][-1]


def _get_information_receiver(context: X12ParserContext) -> Dict:
    """Returns the current information receiver record"""
    information_source = _get_information_source(context)
    return information_source[TransactionLoops.INFORMATION_RECEIVER_LEVEL][-1]


def _get_service_provider(
    context: X12ParserContext, hierarchical_id: str
) -> Optional[Dict]:
    """
    Returns the service provider record by id.

    :param hierarchical_id: The service provider hierarchical level id
    """

    information_receiver = _get_information_receiver(context)

    for sp in information_receiver.get(TransactionLoops.SERVICE_PROVIDER_LEVEL, []):
        sp_hierarchical_id = sp.get("hl_segment", {}).get("hierarchical_id_number")
        if sp_hierarchical_id == hierarchical_id:
            return sp

    return None


def _is_subscriber(patient_record: Dict):
    """Returns true if the patient is a subscriber record"""
    return patient_record.get("hl_segment", {}).get("hierarchical_level_code") == "22"


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
        context.loop_container[TransactionLoops.SERVICE_PROVIDER_NAME] = {}
        loop_record = context.loop_container[TransactionLoops.SERVICE_PROVIDER_NAME]
        context.set_loop_context(TransactionLoops.SERVICE_PROVIDER_NAME, loop_record)


@match("HL", {"hierarchical_level_code": "22"})
def set_subscriber_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the subscriber loop

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    service_provider_id = segment_data.get("hierarchical_parent_id_number")
    service_provider = _get_service_provider(context, service_provider_id)

    if service_provider is None:
        raise LookupError(f"Service Provider ID {service_provider_id} not found")

    if TransactionLoops.SUBSCRIBER_LEVEL not in service_provider:
        service_provider[TransactionLoops.SUBSCRIBER_LEVEL] = []

    service_provider[TransactionLoops.SUBSCRIBER_LEVEL].append({})
    context.subscriber_record = service_provider[TransactionLoops.SUBSCRIBER_LEVEL][-1]
    context.set_loop_context(
        TransactionLoops.SUBSCRIBER_LEVEL, context.subscriber_record
    )
    # subscriber is patient
    if segment_data.get("hierarchical_child_code", "0") == "0":
        context.patient_record = context.subscriber_record


@match("NM1", {"entity_identifier_code": "IL"})
def set_subscriber_name_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the Subscriber Name Loop

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    if context.loop_name == TransactionLoops.SUBSCRIBER_LEVEL:
        context.subscriber_record[TransactionLoops.SUBSCRIBER_NAME] = {}
        loop_record = context.subscriber_record[TransactionLoops.SUBSCRIBER_NAME]
        context.set_loop_context(TransactionLoops.SUBSCRIBER_NAME, loop_record)


@match("TRN")
def set_claim_status_tracking_loop(
    context: X12ParserContext, segment_data: Dict
) -> None:
    """
    Sets the claim status tracking loop for the patient (subscriber or dependent)

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    if _is_subscriber(context.patient_record):
        loop_name = TransactionLoops.SUBSCRIBER_CLAIM_STATUS_TRACKING_NUMBER
    else:
        loop_name = TransactionLoops.DEPENDENT_CLAIM_STATUS_TRACKING_NUMBER

    if loop_name not in context.patient_record:
        context.patient_record[loop_name] = []

    context.patient_record[loop_name].append({"ref_segment": []})
    loop_record = context.patient_record[loop_name][-1]
    context.set_loop_context(loop_name, loop_record)


@match("SVC")
def set_service_line_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the service line loop

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    claim_status = context.loop_container

    if _is_subscriber(context.patient_record):
        loop_name = TransactionLoops.SUBSCRIBER_SERVICE_LINE_INFORMATION
    else:
        loop_name = TransactionLoops.DEPENDENT_SERVICE_LINE_INFORMATION

    if loop_name not in claim_status:
        claim_status[loop_name] = []

    claim_status[loop_name].append({})
    loop_record = claim_status[loop_name][-1]
    context.set_loop_context(loop_name, loop_record)


@match("HL", {"hierarchical_level_code": "23"})
def set_dependent_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the dependent loop
    """
    if TransactionLoops.DEPENDENT_LEVEL not in context.subscriber_record:
        context.subscriber_record[TransactionLoops.DEPENDENT_LEVEL] = []

    context.subscriber_record[TransactionLoops.DEPENDENT_LEVEL].append({})
    context.patient_record = context.subscriber_record[
        TransactionLoops.DEPENDENT_LEVEL
    ][-1]
    context.set_loop_context(TransactionLoops.DEPENDENT_LEVEL, context.patient_record)


@match("NM1", {"entity_identifier_code": "QC"})
def set_dependent_name_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the Dependent Name Loop

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    if context.loop_name == TransactionLoops.DEPENDENT_LEVEL:
        context.patient_record[TransactionLoops.DEPENDENT_NAME] = {}
        loop_record = context.patient_record[TransactionLoops.DEPENDENT_NAME]
        context.set_loop_context(TransactionLoops.DEPENDENT_NAME, loop_record)


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
