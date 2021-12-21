"""
parsing.py

Parses X12 Enrollment 834 005010X220A1 segments into a transactional domain model.

The parsing module includes a specific parser for the 270 transaction and loop parsing functions to create new loops
as segments are streamed to the transactional data model.

Loop parsing functions are implemented as set_[description]_loop(context: X12ParserContext, segment_data: Dict).
"""
from enum import Enum

from linuxforhealth.x12.parsing import match, X12ParserContext
from typing import Dict

# ids for Loop2100G
responsible_person_loop_ids = [
    "6Y",
    "9K",
    "E1",
    "EI",
    "EXS",
    "GB",
    "GD",
    "J6",
    "LR",
    "QD",
    "S1",
    "TZ",
    "X4",
]

loop_2100d_to_2100g_entities = ["36", "M8", "S3"] + responsible_person_loop_ids


class TransactionLoops(str, Enum):
    """
    The loops used to support the 270 005010X279A1 format.
    """

    HEADER = "header"
    SPONSOR_NAME = "loop_1000a"
    PAYER = "loop_1000b"
    TPA_BROKER_NAME = "loop_1000c"
    TPA_BROKER_ACCOUNT_INFORMATION = "loop_1100c"
    MEMBER_LEVEL_DETAIL = "loop_2000"
    MEMBER_NAME = "loop_2100a"
    INCORRECT_MEMBER_NAME = "loop_2100b"
    MEMBER_MAILING_ADDRESS = "loop_2100c"
    MEMBER_EMPLOYER = "loop_2100d"
    MEMBER_SCHOOL = "loop_2100e"
    MEMBER_CUSTODIAL_PARENT = "loop_2100f"
    MEMBER_RESPONSIBLE_PERSON = "loop_2100g"
    MEMBER_DROPOFF_LOCATION = "loop_2100h"
    MEMBER_DISABILITY_INFORMATION = "loop_2200"
    MEMBER_HEALTH_COVERAGE = "loop_2300"
    MEMBER_COVERAGE_PROVIDER_INFORMATION = "loop_2310"
    MEMBER_COVERAGE_COB = "loop_2320"
    MEMBER_COVERAGE_COB_RELATED_ENTITY = "loop_2330"
    MEMBER_REPORTING_CATEGORIES = "loop_2700"
    MEMBER_REPORTING_CATEGORY = "loop_2750"
    FOOTER = "footer"


def _get_tpa_broker(context):
    """Returns the current TPA broker"""
    return context.transaction_data[TransactionLoops.TPA_BROKER_NAME][-1]


def _get_member(context):
    """Returns the current member"""
    return context.transaction_data[TransactionLoops.MEMBER_LEVEL_DETAIL][-1]


def _get_coverage(context):
    """Returns the current coverage"""
    member = _get_member(context)
    return member[TransactionLoops.MEMBER_HEALTH_COVERAGE][-1]


def _get_cob(context):
    """Returns the current cob"""
    coverage = _get_coverage(context)
    return coverage[TransactionLoops.MEMBER_COVERAGE_COB][-1]


def _get_reporting_category(context):
    """Returns the current member reporting category"""
    member = _get_member(context)
    return member[TransactionLoops.MEMBER_REPORTING_CATEGORIES][-1]


@match("ST")
def set_header_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the transaction set header loop for the 270 transaction set.

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment's data
    """

    context.transaction_data[TransactionLoops.HEADER] = {
        "dtp_segment": [],
        "qty_segment": [],
    }

    context.set_loop_context(
        TransactionLoops.HEADER, context.transaction_data[TransactionLoops.HEADER]
    )


@match("N1", conditions={"entity_identifier_code": "P5"})
def set_sponsor_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the sponsor/employer group loop

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment's data
    """

    context.transaction_data[TransactionLoops.SPONSOR_NAME] = {}
    context.set_loop_context(
        TransactionLoops.SPONSOR_NAME,
        context.transaction_data[TransactionLoops.SPONSOR_NAME],
    )


@match("N1", conditions={"entity_identifier_code": "IN"})
def set_payer_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the payer group loop

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment's data
    """

    context.transaction_data[TransactionLoops.PAYER] = {}
    context.set_loop_context(
        TransactionLoops.PAYER, context.transaction_data[TransactionLoops.PAYER]
    )


@match("N1", conditions={"entity_identifier_code": ["BO", "TV"]})
def set_tpa_broker_name_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the TPA/Broker Name loop

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment's data
    """

    if TransactionLoops.TPA_BROKER_NAME not in context.transaction_data:
        context.transaction_data[TransactionLoops.TPA_BROKER_NAME] = []

    context.transaction_data[TransactionLoops.TPA_BROKER_NAME].append({})
    tpa_broker_name = context.transaction_data[TransactionLoops.TPA_BROKER_NAME][-1]
    context.set_loop_context(
        TransactionLoops.TPA_BROKER_NAME,
        tpa_broker_name,
    )


@match("ACT")
def set_tpa_broker_account_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the TPA/Broker Account loop

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment's data
    """
    tpa_broker = _get_tpa_broker(context)
    tpa_broker[TransactionLoops.TPA_BROKER_ACCOUNT_INFORMATION] = {}
    tpa_broker_account = tpa_broker[TransactionLoops.TPA_BROKER_ACCOUNT_INFORMATION]
    context.set_loop_context(
        TransactionLoops.TPA_BROKER_ACCOUNT_INFORMATION, tpa_broker_account
    )


@match("INS")
def set_member_detail_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the Member Detail loop

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment's data
    """
    if TransactionLoops.MEMBER_LEVEL_DETAIL not in context.transaction_data:
        context.transaction_data[TransactionLoops.MEMBER_LEVEL_DETAIL] = []

    context.transaction_data[TransactionLoops.MEMBER_LEVEL_DETAIL].append(
        {"ref_segment": [], "dtp_segment": []}
    )

    member_level_detail = context.transaction_data[
        TransactionLoops.MEMBER_LEVEL_DETAIL
    ][-1]
    context.set_loop_context(TransactionLoops.MEMBER_LEVEL_DETAIL, member_level_detail)


@match("NM1", conditions={"entity_identifier_code": ["74", "IL"]})
def set_member_name_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the member name loop

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment's data
    """
    member_loop = _get_member(context)
    member_loop[TransactionLoops.MEMBER_NAME] = {
        "ec_segment": [],
        "amt_segment": [],
        "lui_segment": [],
    }

    member_name = member_loop[TransactionLoops.MEMBER_NAME]
    context.set_loop_context(TransactionLoops.MEMBER_NAME, member_name)


@match("NM1", conditions={"entity_identifier_code": "70"})
def set_incorrect_member_name_loop(
    context: X12ParserContext, segment_data: Dict
) -> None:
    """
    Sets the member name loop

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment's data
    """
    member_loop = _get_member(context)
    member_loop[TransactionLoops.INCORRECT_MEMBER_NAME] = {}

    incorrect_member_name = member_loop[TransactionLoops.INCORRECT_MEMBER_NAME]
    context.set_loop_context(
        TransactionLoops.INCORRECT_MEMBER_NAME, incorrect_member_name
    )


@match("NM1", conditions={"entity_identifier_code": "31"})
def set_member_mailing_address_loop(
    context: X12ParserContext, segment_data: Dict
) -> None:
    """
    Sets the member mailing address loop

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment's data
    """
    member_loop = _get_member(context)
    member_loop[TransactionLoops.MEMBER_MAILING_ADDRESS] = {}

    member_mailing_address = member_loop[TransactionLoops.MEMBER_MAILING_ADDRESS]
    context.set_loop_context(
        TransactionLoops.MEMBER_MAILING_ADDRESS, member_mailing_address
    )


def _is_responsible_person(entity_identifier: str):
    """Returns true if the entity identifier is used for loop 2100G"""
    return entity_identifier in responsible_person_loop_ids


@match(
    "NM1",
    conditions={"entity_identifier_code": loop_2100d_to_2100g_entities},
)
def set_member_2100d_to_2100g_loop(
    context: X12ParserContext, segment_data: Dict
) -> None:
    """
    Sets the following member entity loops:
    * Loop 2100D - Member Employer
    * Loop 2100E - Member School
    * Loop 2100F - Member Custodial Parent
    * Loop 2100G - Member Responsible Person
    """
    member_loop = _get_member(context)

    entity_identifier = segment_data.get("entity_identifier_code")
    if entity_identifier == "36":
        loop_name = TransactionLoops.MEMBER_EMPLOYER
    elif entity_identifier == "M8":
        loop_name = TransactionLoops.MEMBER_SCHOOL
    elif entity_identifier == "S3":
        loop_name = TransactionLoops.MEMBER_CUSTODIAL_PARENT
    elif _is_responsible_person(entity_identifier):
        loop_name = TransactionLoops.MEMBER_RESPONSIBLE_PERSON
    else:
        raise ValueError(f"Unable to parse entity identifier {entity_identifier}")

    member_loop[loop_name] = {}
    context.set_loop_context(loop_name, member_loop[loop_name])


@match("NM1", conditions={"entity_identifier_code": "45"})
def set_member_drop_off_location_loop(
    context: X12ParserContext, segment_data: Dict
) -> None:
    """
    Sets the member drop off location (shipments) loop

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment's data
    """
    member_loop = _get_member(context)
    member_loop[TransactionLoops.MEMBER_DROPOFF_LOCATION] = {}

    member_dropoff_location = member_loop[TransactionLoops.MEMBER_DROPOFF_LOCATION]
    context.set_loop_context(
        TransactionLoops.MEMBER_DROPOFF_LOCATION, member_dropoff_location
    )


@match("DSB")
def set_member_disability_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the member disability loop

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment's data
    """
    member_loop = _get_member(context)
    member_loop[TransactionLoops.MEMBER_DISABILITY_INFORMATION] = {
        "dsb_segment": [],
        "dtp_segment": [],
    }

    member_disability_information = member_loop[
        TransactionLoops.MEMBER_DISABILITY_INFORMATION
    ]
    context.set_loop_context(
        TransactionLoops.MEMBER_DISABILITY_INFORMATION, member_disability_information
    )


@match("HD")
def set_hd_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the Member health coverage loop.

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment's data
    """
    member = _get_member(context)
    if TransactionLoops.MEMBER_HEALTH_COVERAGE not in member:
        member[TransactionLoops.MEMBER_HEALTH_COVERAGE] = []

    member[TransactionLoops.MEMBER_HEALTH_COVERAGE].append(
        {"dtp_segment": [], "amt_segment": [], "ref_segment": [], "idc_segment": []}
    )

    health_coverage = member[TransactionLoops.MEMBER_HEALTH_COVERAGE][-1]
    context.set_loop_context(TransactionLoops.MEMBER_HEALTH_COVERAGE, health_coverage)


@match("LX")
def set_provider_information_loop(
    context: X12ParserContext, segment_data: Dict
) -> None:
    """
    Sets the Member Coverage Provider Information Loop

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment's data
    """
    if context.loop_name not in (
        TransactionLoops.MEMBER_HEALTH_COVERAGE,
        TransactionLoops.MEMBER_COVERAGE_PROVIDER_INFORMATION,
    ):
        return

    coverage = _get_coverage(context)
    if TransactionLoops.MEMBER_COVERAGE_PROVIDER_INFORMATION not in context:
        coverage[TransactionLoops.MEMBER_COVERAGE_PROVIDER_INFORMATION] = []

    coverage[TransactionLoops.MEMBER_COVERAGE_PROVIDER_INFORMATION].append(
        {"per_segment": []}
    )

    provider_information = coverage[
        TransactionLoops.MEMBER_COVERAGE_PROVIDER_INFORMATION
    ][-1]
    context.set_loop_context(
        TransactionLoops.MEMBER_COVERAGE_PROVIDER_INFORMATION, provider_information
    )


@match("COB")
def set_cob_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the member coverage COB loop

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment's data
    """
    coverage = _get_coverage(context)

    if TransactionLoops.MEMBER_COVERAGE_COB not in coverage:
        coverage[TransactionLoops.MEMBER_COVERAGE_COB] = []

    coverage[TransactionLoops.MEMBER_COVERAGE_COB].append(
        {"ref_segment": [], "dtp_segment": []}
    )

    cob = coverage[TransactionLoops.MEMBER_COVERAGE_COB][-1]
    context.set_loop_context(TransactionLoops.MEMBER_COVERAGE_COB, cob)


@match("NM1", conditions={"entity_identifier_code": ["36", "GW", "IN"]})
def set_cob_related_entity_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the COB related entity loop

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment's data
    """
    if context.loop_name not in (
        TransactionLoops.MEMBER_COVERAGE_COB,
        TransactionLoops.MEMBER_COVERAGE_COB_RELATED_ENTITY,
    ):
        return

    cob = _get_cob(context)

    if TransactionLoops.MEMBER_COVERAGE_COB_RELATED_ENTITY not in cob:
        cob[TransactionLoops.MEMBER_COVERAGE_COB_RELATED_ENTITY] = []

    cob[TransactionLoops.MEMBER_COVERAGE_COB_RELATED_ENTITY].append({})
    related_entity = cob[TransactionLoops.MEMBER_COVERAGE_COB_RELATED_ENTITY][-1]

    context.set_loop_context(
        TransactionLoops.MEMBER_COVERAGE_COB_RELATED_ENTITY, related_entity
    )


@match("LS")
def set_reporting_categories_in_member_loop(
    context: X12ParserContext, segment_data: Dict
) -> None:
    """
    Sets the context to the member loop for the LS segment (additional reporting categories).
    THe LS segment is used to indicate that the 2700 loop follows.

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment's data
    """
    member = _get_member(context)
    context.set_loop_context(TransactionLoops.MEMBER_LEVEL_DETAIL, member)


@match("LX")
def set_member_reporting_categories_loop(
    context: X12ParserContext, segment_data: Dict
) -> None:
    """
    Sets the Member Reporting Categories Loop

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment's data
    """

    if context.loop_name not in (
        TransactionLoops.MEMBER_LEVEL_DETAIL,
        TransactionLoops.MEMBER_REPORTING_CATEGORIES,
    ):
        return

    member = _get_member(context)
    if TransactionLoops.MEMBER_REPORTING_CATEGORIES not in member:
        member[TransactionLoops.MEMBER_REPORTING_CATEGORIES] = []

    member[TransactionLoops.MEMBER_REPORTING_CATEGORIES].append({})

    reporting_categories = member[TransactionLoops.MEMBER_REPORTING_CATEGORIES][-1]
    context.set_loop_context(
        TransactionLoops.MEMBER_REPORTING_CATEGORIES, reporting_categories
    )


@match("N1", conditions={"entity_identifier_code": "75"})
def set_reporting_category_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the reporting category loop (detail information)

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment's data
    """
    reporting_category = _get_reporting_category(context)
    reporting_category[TransactionLoops.MEMBER_REPORTING_CATEGORY] = {}
    report_detail = reporting_category[TransactionLoops.MEMBER_REPORTING_CATEGORY]
    context.set_loop_context(TransactionLoops.MEMBER_REPORTING_CATEGORY, report_detail)


@match("LE")
def set_reporting_categories_end_loop(
    context: X12ParserContext, segment_data: Dict
) -> None:
    """
    Sets the context to the member loop for the LE segment (additional reporting categories termination).
    The LE segment follows the completion of the 2700 loop.

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment's data
    """
    member = _get_member(context)
    context.set_loop_context(TransactionLoops.MEMBER_LEVEL_DETAIL, member)


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
