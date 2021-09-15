"""
parsing.py

Parses X12 837 005010X222A2 segments into a transactional domain model.

The parsing module includes a specific parser for the 837 transaction and loop parsing functions to create new loops
as segments are streamed to the transactional data model.

Loop parsing functions are implemented as set_[description]_loop(context: X12ParserContext).
"""

from enum import Enum
from x12.parsing import match, X12ParserContext
from typing import Dict


class TransactionLoops(str, Enum):
    """
    The loops used to support the 837 005010X222A2 format.
    """

    HEADER = "header"
    SUBMITTER_NAME = "loop_1000a"
    RECEIVER_NAME = "loop_1000b"
    BILLING_PROVIDER = "loop_2000a"
    BILLING_PROVIDER_NAME = "loop_2010aa"
    BILLING_PROVIDER_PAY_TO_ADDRESS = "loop_2010ab"
    BILLING_PROVIDER_PAY_TO_PLAN_NAME = "loop_2010ac"
    SUBSCRIBER = "loop_2000b"
    SUBSCRIBER_NAME = "loop_2010ba"
    SUBSCRIBER_PAYER_NAME = "loop_2010bb"
    PATIENT_LOOP = "loop_2000c"
    PATIENT_LOOP_NAME = "loop_2010ca"
    PATIENT_CLAIM_INFORMATION = "loop_2300"
    CLAIM_REFERRING_PROVIDER_NAME = "loop_2310a"
    CLAIM_RENDERING_PROVIDER_NAME = "loop_2310b"
    CLAIM_SERVICE_FACILITY_LOCATION_NAME = "loop_2310c"
    CLAIM_SUPERVISING_PROVIDER_NAME = "loop_2310d"
    CLAIM_AMBULANCE_PICKUP_LOCATION = "loop_2310e"
    CLAIM_AMBULANCE_DROPOFF_LOCATION = "loop_2310f"
    CLAIM_OTHER_SUBSCRIBER_INFORMATION = "loop_2320"
    CLAIM_OTHER_SUBSCRIBER_NAME = "loop_2330a"
    CLAIM_OTHER_SUBSCRIBER_OTHER_PAYER_NAME = "loop_2330b"
    CLAIM_OTHER_SUBSCRIBER_OTHER_PAYER_REFERRING_PROVIDER_NAME = "loop_2330c"
    CLAIM_OTHER_SUBSCRIBER_OTHER_PAYER_RENDERING_PROVIDER_NAME = "loop_2330d"
    CLAIM_OTHER_SUBSCRIBER_OTHER_PAYER_SERVICE_FACILITY_LOCATION = "loop_2330e"
    CLAIM_OTHER_SUBSCRIBER_OTHER_PAYER_SUPERVISING_PROVIDER_NAME = "loop_2330f"
    CLAIM_OTHER_SUBSCRIBER_OTHER_PAYER_BILLING_PROVIDER_NAME = "loop_2330g"
    CLAIM_SERVICE_LINE = "loop_2400"
    CLAIM_SERVICE_LINE_DRUG_IDENTIFICATION_NAME = "loop_2410"
    CLAIM_SERVICE_LINE_RENDERING_PROVIDER_NAME = "loop_2420a"
    CLAIM_SERVICE_LINE_PURCHASED_SERVICE_PROVIDER_NAME = "loop_2420b"
    CLAIM_SERVICE_LINE_SERVICE_FACILITY_LOCATION_NAME = "loop_2420c"
    CLAIM_SERVICE_LINE_SUPERVISING_PROVIDER_NAME = "loop_2420d"
    CLAIM_SERVICE_LINE_ORDERING_PROVIDER_NAME = "loop_2420e"
    CLAIM_SERVICE_LINE_REFERRING_PROVIDER_NAME = "loop_2420f"
    CLAIM_SERVICE_LINE_AMBULANCE_PICKUP_LOCATION = "loop_2420g"
    CLAIM_SERVICE_LINE_AMBULANCE_DROPOFF_LOCATION = "loop_2420h"
    CLAIM_SERVICE_LINE_LINE_AJUDICATION_INFORMATION = "loop_2430"
    CLAIM_SERVICE_LINE_LINE_FORM_IDENTIFICATION = "loop_2440"
    FOOTER = "footer"


def _get_header(context: X12ParserContext) -> Dict:
    """Returns the 837 transaction header"""
    return context.transaction_data[TransactionLoops.HEADER]

def _get_billing_provider(context: X12ParserContext) -> Dict:
    """Returns the current billing provider record"""
    return context.transaction_data[TransactionLoops.BILLING_PROVIDER][-1]


@match("ST")
def set_header_loop(context: X12ParserContext) -> None:
    """
    Sets the transaction set header loop for the 837 transaction set.

    :param context: The X12Parsing context which contains the current loop and transaction record.
    """

    context.set_loop_context(
        TransactionLoops.HEADER, context.transaction_data[TransactionLoops.HEADER]
    )


@match("NM1")
def set_submitter_name_loop(context: X12ParserContext) -> None:
    """
    Sets the submitter name loop for the 837 transaction set.
    The submitter name loop is nested within the header loop.

    :param context: The X12Parsing context which contains the current loop and transaction record.
    """
    if context.loop_name == TransactionLoops.HEADER:
        context.transaction_data[TransactionLoops.SUBMITTER_NAME] = {"per_segment": []}
        submitter_loop = context.transaction_data[TransactionLoops.SUBMITTER_NAME]
        context.set_loop_context(TransactionLoops.SUBMITTER_NAME, submitter_loop)


@match("NM1", conditions={"entity_identifier_code": "40"})
def set_receiver_name_loop(context: X12ParserContext) -> None:
    """
    Sets the receiver name loop for the 837 transaction set.
    The receiver name loop is nested within the header loop.

    :param context: The X12Parsing context which contains the current loop and transaction record.
    """
    if context.loop_name == TransactionLoops.SUBMITTER_NAME:
        context.transaction_data[TransactionLoops.RECEIVER_NAME] = {}
        receiver_loop = context.transaction_data[TransactionLoops.RECEIVER_NAME]
        context.set_loop_context(TransactionLoops.RECEIVER_NAME, receiver_loop)


@match("HL", conditions={"hierarchical_level_code": "20"})
def set_billing_provider_loop(context: X12ParserContext) -> None:
    """
    Sets the billing provider loop for the 837 transaction set.

    :param context: The X12Parsing context which contains the current loop and transaction record.
    """

    if TransactionLoops.BILLING_PROVIDER not in context.transaction_data:
        context.transaction_data[TransactionLoops.BILLING_PROVIDER] = [{}]
    else:
        context.transaction_data[TransactionLoops.BILLING_PROVIDER].append({})

    billing_provider = context.transaction_data[TransactionLoops.BILLING_PROVIDER][-1]
    context.set_loop_context(TransactionLoops.BILLING_PROVIDER, billing_provider)


@match("NM1", conditions={"entity_identifier_code": "85"})
def set_billing_provider_name_loop(context: X12ParserContext) -> None:
    """
    Sets the billing provider name loop for the 837 transaction set.

    :param context: The X12Parsing context which contains the current loop and transaction record.
    """
    if context.loop_name == TransactionLoops.BILLING_PROVIDER:
        billing_provider = _get_billing_provider(context)
        billing_provider["loop_2010aa"] = {"ref_segment": []}
        billing_provider_name = billing_provider["loop_2010aa"]
        context.set_loop_context(TransactionLoops.BILLING_PROVIDER_NAME, billing_provider_name)


@match("NM1", conditions={"entity_identifier_code": "87"})
def set_pay_to_address_name_loop(context: X12ParserContext) -> None:
    """
    Sets the pay to address name loop for the 837 transaction set.

    :param context: The X12Parsing context which contains the current loop and transaction record.
    """
    if context.loop_name == TransactionLoops.BILLING_PROVIDER_NAME:
        billing_provider = _get_billing_provider(context)
        billing_provider["loop_2010ab"] = {}
        pay_to_address = billing_provider["loop_2010ab"]
        context.set_loop_context(TransactionLoops.BILLING_PROVIDER_PAY_TO_ADDRESS, pay_to_address)


@match("NM1", conditions={"entity_identifier_code": "PE"})
def set_pay_to_plan_name_loop(context: X12ParserContext) -> None:
    """
    Sets the pay to plan name loop for the 837 transaction set.

    :param context: The X12Parsing context which contains the current loop and transaction record.
    """
    if context.loop_name in (TransactionLoops.BILLING_PROVIDER_NAME, TransactionLoops.BILLING_PROVIDER_PAY_TO_ADDRESS):
        billing_provider = _get_billing_provider(context)
        billing_provider["loop_2010ac"] = {"ref_segment": []}
        pay_to_plan = billing_provider["loop_2010ac"]
        context.set_loop_context(TransactionLoops.BILLING_PROVIDER_PAY_TO_PLAN_NAME, pay_to_plan)


@match("SE")
def set_se_loop(context: X12ParserContext) -> None:
    """
    Sets the transaction set footer loop.

    :param context: The X12Parsing context which contains the current loop and transaction record.
    """

    context.set_loop_context(
        TransactionLoops.FOOTER, context.transaction_data["footer"]
    )
