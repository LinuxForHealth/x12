"""
parsing.py

Parses X12 837 005010X222A2 segments into a transactional domain model.

The parsing module includes a specific parser for the 837 transaction and loop parsing functions to create new loops
as segments are streamed to the transactional data model.

Loop parsing functions are implemented as set_[description]_loop(context: X12ParserContext, segment_data: Dict).
"""

from enum import Enum
from x12.parsing import match, X12ParserContext
from typing import Dict, Optional


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
    CLAIM_INFORMATION = "loop_2300"
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


def _get_subscriber(context: X12ParserContext) -> Dict:
    """Returns the current subscriber record"""
    billing_provider = _get_billing_provider(context)
    return billing_provider[TransactionLoops.SUBSCRIBER][-1]


def _get_patient(context: X12ParserContext) -> Optional[Dict]:
    """Returns the current patient record (subscriber or dependent)"""
    subscriber = _get_subscriber(context)
    is_subscriber_patient = (
        subscriber.get("hl_segment", {}).get("hierarchical_child_code", "0") == "0"
    )

    if is_subscriber_patient:
        return subscriber
    else:
        return subscriber.get(TransactionLoops.PATIENT_LOOP, [{}])[-1]


def _is_patient_a_dependent(patient_record: Dict):
    """Returns true if the patient is a dependent record"""
    return patient_record.get("hl_segment", {}).get("hierarchical_level_code") == "23"


def _get_claim(context: X12ParserContext) -> Dict:
    """Returns the current claim record for the patient (either subscriber or dependent)"""
    patient = _get_patient(context)
    if _is_patient_a_dependent(patient):
        claim = patient[TransactionLoops.CLAIM_INFORMATION][-1]
    else:
        subscriber = _get_subscriber(context)
        claim = subscriber[TransactionLoops.CLAIM_INFORMATION][-1]
    return claim


def _get_other_subscriber(context: X12ParserContext) -> Dict:
    """Returns the other subscriber record for the current healthcare claim"""
    claim = _get_claim(context)
    return claim.get(TransactionLoops.CLAIM_OTHER_SUBSCRIBER_INFORMATION, [{}])[-1]


@match("ST")
def set_header_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the transaction set header loop for the 837 transaction set.

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """

    context.set_loop_context(
        TransactionLoops.HEADER, context.transaction_data[TransactionLoops.HEADER]
    )


@match("NM1")
def set_submitter_name_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the submitter name loop for the 837 transaction set.
    The submitter name loop is nested within the header loop.

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    if context.loop_name == TransactionLoops.HEADER:
        context.transaction_data[TransactionLoops.SUBMITTER_NAME] = {"per_segment": []}
        submitter_loop = context.transaction_data[TransactionLoops.SUBMITTER_NAME]
        context.reset_loop_context()
        context.set_loop_context(TransactionLoops.SUBMITTER_NAME, submitter_loop)


@match("NM1", conditions={"entity_identifier_code": "40"})
def set_receiver_name_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the receiver name loop for the 837 transaction set.
    The receiver name loop is nested within the header loop.

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    if context.loop_name == TransactionLoops.SUBMITTER_NAME:
        context.transaction_data[TransactionLoops.RECEIVER_NAME] = {}
        receiver_loop = context.transaction_data[TransactionLoops.RECEIVER_NAME]
        context.reset_loop_context()
        context.set_loop_context(TransactionLoops.RECEIVER_NAME, receiver_loop)


@match("HL", conditions={"hierarchical_level_code": "20"})
def set_billing_provider_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the billing provider loop for the 837 transaction set.

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    context.reset_loop_context()

    if TransactionLoops.BILLING_PROVIDER not in context.transaction_data:
        context.transaction_data[TransactionLoops.BILLING_PROVIDER] = [{}]
    else:
        context.transaction_data[TransactionLoops.BILLING_PROVIDER].append({})

    billing_provider = context.transaction_data[TransactionLoops.BILLING_PROVIDER][-1]
    context.set_loop_context(TransactionLoops.BILLING_PROVIDER, billing_provider)


@match("NM1", conditions={"entity_identifier_code": "85"})
def set_billing_provider_name_loop(
    context: X12ParserContext, segment_data: Dict
) -> None:
    """
    Sets the billing provider name loop for the 837 transaction set.

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    if context.loop_name == TransactionLoops.BILLING_PROVIDER:
        billing_provider = _get_billing_provider(context)
        billing_provider[TransactionLoops.BILLING_PROVIDER_NAME] = {"ref_segment": []}
        billing_provider_name = billing_provider[TransactionLoops.BILLING_PROVIDER_NAME]
        context.set_loop_context(
            TransactionLoops.BILLING_PROVIDER_NAME, billing_provider_name
        )


@match("NM1", conditions={"entity_identifier_code": "87"})
def set_pay_to_address_name_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the pay to address name loop for the 837 transaction set.

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    if context.loop_name == TransactionLoops.BILLING_PROVIDER_NAME:
        billing_provider = _get_billing_provider(context)
        billing_provider[TransactionLoops.BILLING_PROVIDER_PAY_TO_ADDRESS] = {}
        pay_to_address = billing_provider[
            TransactionLoops.BILLING_PROVIDER_PAY_TO_ADDRESS
        ]
        context.set_loop_context(
            TransactionLoops.BILLING_PROVIDER_PAY_TO_ADDRESS, pay_to_address
        )


@match("NM1", conditions={"entity_identifier_code": "PE"})
def set_pay_to_plan_name_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the pay to plan name loop for the 837 transaction set.

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    if context.loop_name in (
        TransactionLoops.BILLING_PROVIDER_NAME,
        TransactionLoops.BILLING_PROVIDER_PAY_TO_ADDRESS,
    ):
        billing_provider = _get_billing_provider(context)
        billing_provider[TransactionLoops.BILLING_PROVIDER_PAY_TO_PLAN_NAME] = {
            "ref_segment": []
        }
        pay_to_plan = billing_provider[
            TransactionLoops.BILLING_PROVIDER_PAY_TO_PLAN_NAME
        ]
        context.set_loop_context(
            TransactionLoops.BILLING_PROVIDER_PAY_TO_PLAN_NAME, pay_to_plan
        )


@match("HL", conditions={"hierarchical_level_code": "22"})
def set_subscriber_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the subscriber loop for the 837 transaction set.

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    billing_provider = _get_billing_provider(context)

    if TransactionLoops.SUBSCRIBER not in billing_provider:
        billing_provider[TransactionLoops.SUBSCRIBER] = [{}]
    else:
        billing_provider[TransactionLoops.SUBSCRIBER].append({})

    subscriber = billing_provider[TransactionLoops.SUBSCRIBER][-1]

    if TransactionLoops.PATIENT_LOOP not in subscriber:
        subscriber[TransactionLoops.PATIENT_LOOP] = [{}]

    context.set_loop_context(TransactionLoops.SUBSCRIBER, subscriber)


@match("NM1", conditions={"entity_identifier_code": "IL"})
def set_subscriber_name_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the subscriber name for the 837 transaction set

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    if context.loop_name == TransactionLoops.SUBSCRIBER:
        subscriber = _get_subscriber(context)
        subscriber[TransactionLoops.SUBSCRIBER_NAME] = {"ref_segment": []}
        subscriber_name = subscriber[TransactionLoops.SUBSCRIBER_NAME]
        context.set_loop_context(TransactionLoops.SUBSCRIBER_NAME, subscriber_name)


@match("NM1", conditions={"entity_identifier_code": "PR"})
def set_payer_name_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the payer name for the 837 transaction set

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    if context.loop_name == TransactionLoops.SUBSCRIBER_NAME:
        subscriber = _get_subscriber(context)
        subscriber[TransactionLoops.SUBSCRIBER_PAYER_NAME] = {"ref_segment": []}
        payer_name = subscriber[TransactionLoops.SUBSCRIBER_PAYER_NAME]
        context.set_loop_context(TransactionLoops.SUBSCRIBER_PAYER_NAME, payer_name)


@match("HL", conditions={"hierarchical_level_code": "23"})
def set_patient_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the patient loop.
    The patient loop is used when the patient is not the subscriber, or cannot be identified as a subscriber.

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    subscriber = _get_subscriber(context)
    patient_loop = subscriber[TransactionLoops.PATIENT_LOOP][-1]
    context.set_loop_context(TransactionLoops.PATIENT_LOOP, patient_loop)


@match("NM1", conditions={"entity_identifier_code": "QC"})
def set_patient_name_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the patient name loop

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    patient = _get_patient(context)

    if TransactionLoops.PATIENT_LOOP_NAME not in patient:
        patient[TransactionLoops.PATIENT_LOOP_NAME] = {}

    patient_name = patient[TransactionLoops.PATIENT_LOOP_NAME]
    context.set_loop_context(TransactionLoops.PATIENT_LOOP_NAME, patient_name)


@match("CLM")
def set_claim_information_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the claim information loop for a subscriber or dependent

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    is_dependent_claim = (
        _get_subscriber(context)
        .get("hl_segment", {})
        .get("hierarchical_child_code", "0")
        == "1"
    )

    if not is_dependent_claim:
        patient = _get_subscriber(context)
    else:
        patient = _get_patient(context)

    patient_claim = {
        "dtp_segment": [],
        "ref_segment": [],
        "pwk_segment": [],
        "k3_segment": [],
        "crc_segment": [],
        "hi_segment": [],
    }

    if TransactionLoops.CLAIM_INFORMATION not in patient:
        patient[TransactionLoops.CLAIM_INFORMATION] = [patient_claim]
    else:
        patient[TransactionLoops.CLAIM_INFORMATION].append(patient_claim)

    patient_claim = patient[TransactionLoops.CLAIM_INFORMATION][-1]
    context.set_loop_context(TransactionLoops.CLAIM_INFORMATION, patient_claim)


@match(
    "NM1",
    conditions={"entity_identifier_code": ["DN", "P3", "B2", "77", "DQ", "PW", "45"]},
)
def set_claim_sub_loop(context: X12ParserContext, segment_data: Dict):
    """
    Matches Claim 2300 "sub-loops" 2310A-2310F

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    if TransactionLoops.CLAIM_INFORMATION not in context.parsed_loops:
        return

    identifier_code = segment_data.get("entity_identifier_code")
    claim = _get_claim(context)

    if identifier_code in ("DN", "P3"):
        claim[TransactionLoops.CLAIM_REFERRING_PROVIDER_NAME] = {"ref_segment": []}
        rendering_provider = claim[TransactionLoops.CLAIM_REFERRING_PROVIDER_NAME]
        context.set_loop_context(
            TransactionLoops.CLAIM_REFERRING_PROVIDER_NAME, rendering_provider
        )
    elif identifier_code == "B2":
        claim[TransactionLoops.CLAIM_RENDERING_PROVIDER_NAME] = {"ref_segment": []}
        rendering_provider = claim[TransactionLoops.CLAIM_RENDERING_PROVIDER_NAME]
        context.set_loop_context(
            TransactionLoops.CLAIM_RENDERING_PROVIDER_NAME, rendering_provider
        )
    elif identifier_code == "77":
        claim[TransactionLoops.CLAIM_SERVICE_FACILITY_LOCATION_NAME] = {
            "ref_segment": []
        }
        service_facility = claim[TransactionLoops.CLAIM_SERVICE_FACILITY_LOCATION_NAME]
        context.set_loop_context(
            TransactionLoops.CLAIM_SERVICE_FACILITY_LOCATION_NAME, service_facility
        )
    elif identifier_code == "DQ":
        claim[TransactionLoops.CLAIM_SUPERVISING_PROVIDER_NAME] = {"ref_segment": []}
        supervising_provider = claim[TransactionLoops.CLAIM_SUPERVISING_PROVIDER_NAME]
        context.set_loop_context(
            TransactionLoops.CLAIM_SUPERVISING_PROVIDER_NAME, supervising_provider
        )
    elif identifier_code == "PW":
        claim[TransactionLoops.CLAIM_AMBULANCE_PICKUP_LOCATION] = {}
        ambulance_pickup = claim[TransactionLoops.CLAIM_AMBULANCE_PICKUP_LOCATION]
        context.set_loop_context(
            TransactionLoops.CLAIM_AMBULANCE_PICKUP_LOCATION, ambulance_pickup
        )
    elif identifier_code == "45":
        claim[TransactionLoops.CLAIM_AMBULANCE_DROPOFF_LOCATION] = {}
        ambulance_dropoff = claim[TransactionLoops.CLAIM_AMBULANCE_DROPOFF_LOCATION]
        context.set_loop_context(
            TransactionLoops.CLAIM_AMBULANCE_DROPOFF_LOCATION, ambulance_dropoff
        )


@match("SBR")
def set_other_subscriber(context: X12ParserContext, segment_data: Dict):
    """
    Sets the claim other subscriber loop used to coordinate payment and other insurance carriers.

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    if TransactionLoops.CLAIM_INFORMATION in context.parsed_loops:
        claim = _get_claim(context)
        other_subscriber = {"cas_segment": [], "amt_segment": []}

        if TransactionLoops.CLAIM_OTHER_SUBSCRIBER_INFORMATION not in claim:
            claim[TransactionLoops.CLAIM_OTHER_SUBSCRIBER_INFORMATION] = [
                other_subscriber
            ]
        else:
            claim[TransactionLoops.CLAIM_OTHER_SUBSCRIBER_INFORMATION].append(
                other_subscriber
            )

        other_subscriber = claim[TransactionLoops.CLAIM_OTHER_SUBSCRIBER_INFORMATION][
            -1
        ]
        context.set_loop_context(
            TransactionLoops.CLAIM_OTHER_SUBSCRIBER_INFORMATION, other_subscriber
        )


@match("NM1", conditions={"entity_identifier_code": "IL"})
def set_other_subscriber_name(context: X12ParserContext, segment_data: Dict):
    """
    Sets the claim other subscriber name loop.

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """

    if TransactionLoops.CLAIM_OTHER_SUBSCRIBER_INFORMATION in context.parsed_loops:
        other_subscriber = _get_other_subscriber(context)

        if TransactionLoops.CLAIM_OTHER_SUBSCRIBER_NAME not in other_subscriber:
            other_subscriber[TransactionLoops.CLAIM_OTHER_SUBSCRIBER_NAME] = {}

        context.set_loop_context(
            TransactionLoops.CLAIM_OTHER_SUBSCRIBER_NAME,
            other_subscriber[TransactionLoops.CLAIM_OTHER_SUBSCRIBER_NAME],
        )


@match(
    "NM1",
    conditions={"entity_identifier_code": ["PR", "DN", "P3", "82", "77", "DQ", "85"]},
)
def set_other_subscriber_other_payer_loop(
    context: X12ParserContext, segment_data: Dict
):
    """
    Sets the other subscriber other payer information for loops 2330B - 2330G

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    if TransactionLoops.CLAIM_OTHER_SUBSCRIBER_INFORMATION not in context.parsed_loops:
        return

    other_subscriber = _get_other_subscriber(context)
    identifier_code = segment_data.get("entity_identifier_code")

    if identifier_code == "PR":
        loop_name = TransactionLoops.CLAIM_OTHER_SUBSCRIBER_OTHER_PAYER_NAME
    elif identifier_code in ("DN", "P3"):
        loop_name = (
            TransactionLoops.CLAIM_OTHER_SUBSCRIBER_OTHER_PAYER_REFERRING_PROVIDER_NAME
        )
    elif identifier_code == "82":
        loop_name = (
            TransactionLoops.CLAIM_OTHER_SUBSCRIBER_OTHER_PAYER_RENDERING_PROVIDER_NAME
        )
    elif identifier_code == "77":
        loop_name = (
            TransactionLoops.CLAIM_OTHER_SUBSCRIBER_OTHER_PAYER_SERVICE_FACILITY_LOCATION
        )
    elif identifier_code == "DQ":
        loop_name = (
            TransactionLoops.CLAIM_OTHER_SUBSCRIBER_OTHER_PAYER_SUPERVISING_PROVIDER_NAME
        )
    elif identifier_code == "85":
        loop_name = (
            TransactionLoops.CLAIM_OTHER_SUBSCRIBER_OTHER_PAYER_BILLING_PROVIDER_NAME
        )
    else:
        loop_name = None

    if not loop_name:
        raise RuntimeError(
            f"Unable to assign loop to other subscriber identifier {identifier_code}"
        )

    if (
        loop_name
        == TransactionLoops.CLAIM_OTHER_SUBSCRIBER_OTHER_PAYER_REFERRING_PROVIDER_NAME
    ):
        if loop_name not in other_subscriber:
            other_subscriber[loop_name] = [{"ref_segment": []}]
        else:
            other_subscriber[loop_name].append({"ref_segment": {}})
        loop_record = other_subscriber[loop_name][-1]
    else:
        other_subscriber[loop_name] = {"ref_segment": []}
        loop_record = other_subscriber[loop_name]

    context.set_loop_context(loop_name, loop_record)


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
