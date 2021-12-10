"""
parsing.py

Parses X12 837 004010X098A1 segments into a transactional domain model.

The parsing module includes a specific parser for the 837 transaction and loop parsing functions to create new loops
as segments are streamed to the transactional data model.

Loop parsing functions are implemented as set_[description]_loop(context: X12ParserContext, segment_data: Dict).
"""

from enum import Enum
from linuxforhealth.x12.parsing import match, X12ParserContext
from typing import Dict


class TransactionLoops(str, Enum):
    """
    The loops used to support the 837 004010X098A1 format.
    """

    HEADER = "header"
    SUBMITTER_NAME = "loop_1000a"
    RECEIVER_NAME = "loop_1000b"
    BILLING_PROVIDER = "loop_2000a"
    BILLING_PROVIDER_NAME = "loop_2010aa"
    PAY_TO_PROVIDER_NAME = "loop_2010ab"
    SUBSCRIBER = "loop_2000b"
    SUBSCRIBER_NAME = "loop_2010ba"
    SUBSCRIBER_CREDIT_DEBIT_ACCOUNT_HOLDER = "loop_2010bb"
    SUBSCRIBER_PAYER_NAME = "loop_2010bc"
    SUBSCRIBER_RESPONSIBLE_PARTY_NAME = "loop_2010bd"
    PATIENT_LOOP = "loop_2000c"
    PATIENT_LOOP_NAME = "loop_2010ca"
    CLAIM_INFORMATION = "loop_2300"
    CLAIM_HOME_HEALTH_CARE_PLAN = "loop_2305"
    CLAIM_ATTENDING_PHYSICIAN_NAME = "loop_2310a"
    CLAIM_OPERATING_PHYSICIAN_NAME = "loop_2310b"
    CLAIM_OTHER_PROVIDER_NAME = "loop_2310c"
    CLAIM_SERVICE_FACILITY_LOCATION = "loop_2310e"
    CLAIM_OTHER_SUBSCRIBER_INFORMATION = "loop_2320"
    CLAIM_OTHER_SUBSCRIBER_NAME = "loop_2330a"
    CLAIM_OTHER_SUBSCRIBER_OTHER_PAYER_NAME = "loop_2330b"
    CLAIM_OTHER_SUBSCRIBER_OTHER_PAYER_PATIENT_INFORMATION = "loop_2330c"
    CLAIM_OTHER_SUBSCRIBER_OTHER_PAYER_ATTENDING_PROVIDER_NAME = "loop_2330d"
    CLAIM_OTHER_SUBSCRIBER_OTHER_PAYER_OPERATING_PROVIDER = "loop_2330e"
    CLAIM_OTHER_SUBSCRIBER_OTHER_PAYER_OTHER_PROVIDER = "loop_2330f"
    CLAIM_OTHER_SUBSCRIBER_OTHER_PAYER_SERVICE_FACILITY_PROVIDER = "loop_2330h"
    CLAIM_SERVICE_LINE = "loop_2400"
    CLAIM_SERVICE_LINE_DRUG_IDENTIFICATION_NAME = "loop_2410"
    CLAIM_SERVICE_LINE_ATTENDING_PHYSICIAN_NAME = "loop_2420a"
    CLAIM_SERVICE_LINE_OPERATING_PHYSICIAN_NAME = "loop_2420b"
    CLAIM_SERVICE_LINE_OTHER_PROVIDER_NAME = "loop_2420c"
    CLAIM_SERVICE_LINE_LINE_ADJUDICATION_INFORMATION = "loop_2430"
    FOOTER = "footer"


def _get_header(context: X12ParserContext) -> Dict:
    """Returns the 837 transaction header"""
    return context.transaction_data[TransactionLoops.HEADER]


def _get_billing_provider(context: X12ParserContext) -> Dict:
    """Returns the current billing provider record"""
    return context.transaction_data[TransactionLoops.BILLING_PROVIDER][-1]


def _is_patient_a_dependent(patient_record: Dict):
    """Returns true if the patient is a dependent record"""
    return patient_record.get("hl_segment", {}).get("hierarchical_level_code") == "23"


def _get_claim(context: X12ParserContext) -> Dict:
    """Returns the current claim record for the patient (either subscriber or dependent)"""
    if _is_patient_a_dependent(context.patient_record):
        claim = context.patient_record[TransactionLoops.CLAIM_INFORMATION][-1]
    else:
        claim = context.subscriber_record[TransactionLoops.CLAIM_INFORMATION][-1]
    return claim


def _get_other_subscriber(context: X12ParserContext) -> Dict:
    """Returns the other subscriber record for the current healthcare claim"""
    claim = _get_claim(context)
    return claim.get(TransactionLoops.CLAIM_OTHER_SUBSCRIBER_INFORMATION, [{}])[-1]


def _get_service_line(context: X12ParserContext) -> Dict:
    """Returns the current claim service line for the patieht (either subscriber or dependent)"""
    claim = _get_claim(context)
    return claim[TransactionLoops.CLAIM_SERVICE_LINE][-1]


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


@match("NM1", conditions={"entity_identifier_code": "41"})
def set_submitter_name_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Set the Header Submitter Name Loop 1000A

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    if context.loop_name == TransactionLoops.HEADER:
        context.transaction_data[TransactionLoops.SUBMITTER_NAME] = {"per_segment": []}
        submitter_loop = context.transaction_data[TransactionLoops.SUBMITTER_NAME]
        context.set_loop_context(TransactionLoops.SUBMITTER_NAME, submitter_loop)


@match("NM1", conditions={"entity_identifier_code": "40"})
def set_receiver_name_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Set the Header Receiver Name Loop 1000B

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    if context.loop_name == TransactionLoops.SUBMITTER_NAME:
        context.transaction_data[TransactionLoops.RECEIVER_NAME] = {}
        receiver_loop = context.transaction_data[TransactionLoops.RECEIVER_NAME]
        context.set_loop_context(TransactionLoops.RECEIVER_NAME, receiver_loop)


@match("HL", conditions={"hierarchical_level_code": "20"})
def set_billing_provider_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the Billing Provider Loop 2000A

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    if TransactionLoops.BILLING_PROVIDER not in context.transaction_data:
        context.transaction_data[TransactionLoops.BILLING_PROVIDER] = []

    context.transaction_data[TransactionLoops.BILLING_PROVIDER].append({})
    billing_provider_loop = context.transaction_data[TransactionLoops.BILLING_PROVIDER][
        -1
    ]
    context.set_loop_context(TransactionLoops.BILLING_PROVIDER, billing_provider_loop)


@match("NM1", conditions={"entity_identifier_code": "85"})
def set_billing_provider_name_loop(
    context: X12ParserContext, segment_data: Dict
) -> None:
    """
    Sets the Billing Provider Name Loop 2010AA

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    if context.loop_name == TransactionLoops.BILLING_PROVIDER:
        billing_provider = _get_billing_provider(context)

        if TransactionLoops.BILLING_PROVIDER_NAME not in billing_provider:
            billing_provider[TransactionLoops.BILLING_PROVIDER_NAME] = {
                "ref_segment": [],
                "per_segment": [],
            }
        billing_provider_name_loop = billing_provider[
            TransactionLoops.BILLING_PROVIDER_NAME
        ]
        context.set_loop_context(
            TransactionLoops.BILLING_PROVIDER_NAME, billing_provider_name_loop
        )


@match("NM1", conditions={"entity_identifier_code": "87"})
def set_pay_to_provider_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the Pay to Provider Name Loop 2010AB

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    if "loop_2010a" in context.loop_name:
        billing_provider = _get_billing_provider(context)

        if TransactionLoops.PAY_TO_PROVIDER_NAME not in billing_provider:
            billing_provider[TransactionLoops.PAY_TO_PROVIDER_NAME] = {
                "ref_segment": [],
            }
            pay_to_address_loop = billing_provider[
                TransactionLoops.PAY_TO_PROVIDER_NAME
            ]
            context.set_loop_context(
                TransactionLoops.PAY_TO_PROVIDER_NAME, pay_to_address_loop
            )


@match("HL", conditions={"hierarchical_level_code": "22"})
def set_subscriber_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the subscriber loop 2000B

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """

    billing_provider = _get_billing_provider(context)

    if TransactionLoops.SUBSCRIBER not in billing_provider:
        billing_provider[TransactionLoops.SUBSCRIBER] = []

    billing_provider[TransactionLoops.SUBSCRIBER].append({})
    context.subscriber_record = billing_provider[TransactionLoops.SUBSCRIBER][-1]
    context.set_loop_context(TransactionLoops.SUBSCRIBER, context.subscriber_record)

    if context.hl_segment.get("hierarchical_child_code", "0") == "0":
        context.patient_record = context.subscriber_record


@match("NM1", conditions={"entity_identifier_code": "IL"})
def set_subscriber_name_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the subscriber name loop 2010BA

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """

    if context.loop_name == TransactionLoops.SUBSCRIBER:

        if TransactionLoops.SUBSCRIBER_NAME not in context.subscriber_record:
            context.subscriber_record[TransactionLoops.SUBSCRIBER_NAME] = {
                "ref_segment": []
            }

        subscriber_name_loop = context.subscriber_record[
            TransactionLoops.SUBSCRIBER_NAME
        ]
        context.set_loop_context(TransactionLoops.SUBSCRIBER_NAME, subscriber_name_loop)


@match("NM1", conditions={"entity_identifier_code": "AO"})
def set_subscriber_account_holder_loop(
    context: X12ParserContext, segment_data: Dict
) -> None:
    """
    Sets the subscriber debit/credit card account loop 2010BB

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    if "2010b" in context.loop_name:
        context.subscriber_record[
            TransactionLoops.SUBSCRIBER_CREDIT_DEBIT_ACCOUNT_HOLDER
        ] = {"ref_segment": []}
        account_holder = context.subscriber_record[
            TransactionLoops.SUBSCRIBER_CREDIT_DEBIT_ACCOUNT_HOLDER
        ]
        context.set_loop_context(
            TransactionLoops.SUBSCRIBER_CREDIT_DEBIT_ACCOUNT_HOLDER, account_holder
        )


@match("NM1", conditions={"entity_identifier_code": "PR"})
def set_subscriber_payer_name_loop(
    context: X12ParserContext, segment_data: Dict
) -> None:
    """
    Sets the subscriber payer name loop 2010BB

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    if "2010b" in context.loop_name:

        if TransactionLoops.SUBSCRIBER_PAYER_NAME not in context.subscriber_record:
            context.subscriber_record[TransactionLoops.SUBSCRIBER_PAYER_NAME] = {
                "ref_segment": []
            }

        subscriber_payer_name_loop = context.subscriber_record[
            TransactionLoops.SUBSCRIBER_PAYER_NAME
        ]
        context.set_loop_context(
            TransactionLoops.SUBSCRIBER_NAME, subscriber_payer_name_loop
        )


@match(segment_name="NM1", conditions={"entity_identifier_code": "QD"})
def set_subscriber_responsible_party_name(
    context: X12ParserContext, segment_data: Dict
) -> None:
    """
    Sets the Subscriber Responsible Party Name loop 2010bc

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    if "2010b" in context.loop_name:
        context.subscriber_record[
            TransactionLoops.SUBSCRIBER_RESPONSIBLE_PARTY_NAME
        ] = {}
        context.set_loop_context(
            TransactionLoops.SUBSCRIBER_RESPONSIBLE_PARTY_NAME,
            context.subscriber_record[
                TransactionLoops.SUBSCRIBER_RESPONSIBLE_PARTY_NAME
            ],
        )


@match("HL", conditions={"hierarchical_level_code": "23"})
def set_patient_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the patient loop 2000C

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    if TransactionLoops.PATIENT_LOOP not in context.subscriber_record:
        context.subscriber_record[TransactionLoops.PATIENT_LOOP] = []

    context.subscriber_record[TransactionLoops.PATIENT_LOOP].append({})
    context.patient_record = context.subscriber_record[TransactionLoops.PATIENT_LOOP][
        -1
    ]
    context.set_loop_context(TransactionLoops.PATIENT_LOOP, context.patient_record)


@match("NM1", conditions={"entity_identifier_code": "QC"})
def set_patient_name_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the patient name loop 2010CA

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    context.patient_record[TransactionLoops.PATIENT_LOOP_NAME] = {"ref_segment": []}
    patient_name_loop = context.patient_record[TransactionLoops.PATIENT_LOOP_NAME]
    context.set_loop_context(TransactionLoops.PATIENT_LOOP_NAME, patient_name_loop)


@match("CLM")
def set_claim_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the claim loop 2300

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    if TransactionLoops.CLAIM_INFORMATION not in context.patient_record:
        context.patient_record[TransactionLoops.CLAIM_INFORMATION] = []

    context.patient_record[TransactionLoops.CLAIM_INFORMATION].append(
        {
            "dtp_segment": [],
            "pwk_segment": [],
            "amt_segment": [],
            "ref_segment": [],
            "k3_segment": [],
            "crc_segment": [],
            "hi_segment": [],
            "qty_segment": [],
        }
    )

    claim_loop = context.patient_record[TransactionLoops.CLAIM_INFORMATION][-1]
    context.set_loop_context(TransactionLoops.CLAIM_INFORMATION, claim_loop)


@match(
    "NM1",
    conditions={"entity_identifier_code": ["71", "72", "73", "FA"]},
)
def set_claim_entity_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the "entity" loops within the 2300 claims loop, including:
    * Attending Physician Name - Loop 2310A
    * Operating Physician Name - Loop 2310B
    * Other Provider Name - Loop 2310C
    * Service Facility Location- Loop 2310E
    """
    if "loop_2300" in context.loop_name or "loop_2310" in context.loop_name:
        identifier = segment_data.get("entity_identifier_code")
        loop_name = None

        if identifier == "71":
            loop_name = TransactionLoops.CLAIM_ATTENDING_PHYSICIAN_NAME
        elif identifier == "72":
            loop_name = TransactionLoops.CLAIM_OPERATING_PHYSICIAN_NAME
        elif identifier == "73":
            loop_name = TransactionLoops.CLAIM_OTHER_PROVIDER_NAME
        elif identifier == "FA":
            loop_name = TransactionLoops.CLAIM_SERVICE_FACILITY_LOCATION

        if not loop_name:
            raise ValueError(
                f"unable to map identifier {identifier} to a claim entity loop"
            )

        claim = _get_claim(context)
        if loop_name not in claim:
            claim[loop_name] = {"ref_segment": []}

        loop_record = claim[loop_name]
        context.set_loop_context(loop_name, loop_record)


@match("SBR")
def set_other_subscriber_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the claim other subscriber loop 2320

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    if "loop_23" in context.loop_name:
        claim = _get_claim(context)
        if TransactionLoops.CLAIM_OTHER_SUBSCRIBER_INFORMATION not in claim:
            claim[TransactionLoops.CLAIM_OTHER_SUBSCRIBER_INFORMATION] = []

        claim[TransactionLoops.CLAIM_OTHER_SUBSCRIBER_INFORMATION].append(
            {
                "cas_segment": [],
                "amt_segment": [],
            }
        )
        other_subscriber_loop = claim[
            TransactionLoops.CLAIM_OTHER_SUBSCRIBER_INFORMATION
        ][-1]
        context.set_loop_context(
            TransactionLoops.CLAIM_OTHER_SUBSCRIBER_INFORMATION, other_subscriber_loop
        )


@match("NM1", conditions={"entity_identifier_code": "IL"})
def set_other_subscriber_name_loop(
    context: X12ParserContext, segment_data: Dict
) -> None:
    """
    Sets the claim other subscriber name loop 2330A

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    if context.loop_name == TransactionLoops.CLAIM_OTHER_SUBSCRIBER_INFORMATION:
        other_subscriber = _get_other_subscriber(context)
        other_subscriber[TransactionLoops.CLAIM_OTHER_SUBSCRIBER_NAME] = {}

        other_subscriber_name = other_subscriber[
            TransactionLoops.CLAIM_OTHER_SUBSCRIBER_NAME
        ]
        context.set_loop_context(
            TransactionLoops.CLAIM_OTHER_SUBSCRIBER_NAME, other_subscriber_name
        )


@match(
    "NM1",
    conditions={"entity_identifier_code": ["PR", "QC", "71", "72", "73"]},
)
def set_other_subscriber_entities_loop(
    context: X12ParserContext, segment_data: Dict
) -> None:
    """
    Sets the "2330x" entity loops within the Other Subscriber Loop (2320)
    * Other Payer Name - Loop 2330B
    * Other Payer Patient Information Provider - Loop 2330C
    * Other Payer Attending Provider - Loop 2330D
    * Other Payer Operating Provider - 2330E
    * Other Payer Other Provider - 2330F
    * Other Payer Service Facility Provider  2330H
    """
    if "loop_2330" in context.loop_name:
        identifier = segment_data.get("entity_identifier_code")
        loop_name = None

        if identifier == "PR":
            # loop 2330b
            loop_name = TransactionLoops.CLAIM_OTHER_SUBSCRIBER_OTHER_PAYER_NAME
        elif identifier == "QC":
            # loop 2330c
            loop_name = (
                TransactionLoops.CLAIM_OTHER_SUBSCRIBER_OTHER_PAYER_PATIENT_INFORMATION
            )
        elif identifier == "71":
            # loop 2330d
            loop_name = (
                TransactionLoops.CLAIM_OTHER_SUBSCRIBER_OTHER_PAYER_ATTENDING_PROVIDER_NAME
            )
        elif identifier == "72":
            # loop 2330e
            loop_name = (
                TransactionLoops.CLAIM_OTHER_SUBSCRIBER_OTHER_PAYER_OPERATING_PROVIDER
            )
        elif identifier == "73":
            # loop 2330f
            loop_name = (
                TransactionLoops.CLAIM_OTHER_SUBSCRIBER_OTHER_PAYER_OTHER_PROVIDER
            )
        elif identifier == "FA":
            # loop 2330h
            loop_name = (
                TransactionLoops.CLAIM_OTHER_SUBSCRIBER_OTHER_PAYER_SERVICE_FACILITY_LOCATION
            )

        if not loop_name:
            raise ValueError(
                f"unable to map identifier {identifier} to a claim entity loop"
            )

        other_subscriber = _get_other_subscriber(context)
        other_subscriber[loop_name] = {"ref_segment": []}
        context.set_loop_context(loop_name, other_subscriber[loop_name])


@match("LX")
def set_service_line_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the claim service line loop 2400

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    claim = _get_claim(context)

    if TransactionLoops.CLAIM_SERVICE_LINE not in claim:
        claim[TransactionLoops.CLAIM_SERVICE_LINE] = []

    claim[TransactionLoops.CLAIM_SERVICE_LINE].append(
        {
            "pwk_segment": [],
            "dtp_segment": [],
            "amt_segment": [],
        }
    )

    service_line_loop = claim[TransactionLoops.CLAIM_SERVICE_LINE][-1]
    context.set_loop_context(TransactionLoops.CLAIM_SERVICE_LINE, service_line_loop)


@match("LIN")
def set_drug_identification_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the service line drug identification loop 2410

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    if "loop_24" in context.loop_name:
        service_line = _get_service_line(context)
        service_line[TransactionLoops.CLAIM_SERVICE_LINE_DRUG_IDENTIFICATION_NAME] = {}
        loop_record = service_line[
            TransactionLoops.CLAIM_SERVICE_LINE_DRUG_IDENTIFICATION_NAME
        ]
        context.set_loop_context(
            TransactionLoops.CLAIM_SERVICE_LINE_DRUG_IDENTIFICATION_NAME, loop_record
        )


@match(
    "NM1",
    conditions={"entity_identifier_code": ["71", "72", "73"]},
)
def set_service_line_entities_loop(
    context: X12ParserContext, segment_data: Dict
) -> None:
    """
    Sets the entities within the service line loop 2400:
    * Attending Physician Name- Loop 2420A
    * Operating Physician Name - Loop 2420B
    * Other Provider Name - Loop 2420C

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    if "loop_24" in context.loop_name:
        identifier = segment_data.get("entity_identifier_code")
        loop_name = None

        if identifier == "71":
            # loop 2420A
            loop_name = TransactionLoops.CLAIM_SERVICE_LINE_ATTENDING_PHYSICIAN_NAME
        elif identifier == "72":
            # loop 2420B
            loop_name = TransactionLoops.CLAIM_SERVICE_LINE_OPERATING_PHYSICIAN_NAME
        elif identifier == "73":
            # loop 2420C
            loop_name = TransactionLoops.CLAIM_SERVICE_LINE_OTHER_PROVIDER_NAME

        if not loop_name:
            raise ValueError(
                f"unable to map identifier {identifier} to a claim entity loop"
            )
        service_line = _get_service_line(context)
        service_line[loop_name] = {"ref_segment": []}
        loop_record = service_line[loop_name]
        context.set_loop_context(loop_name, loop_record)


@match("SVD")
def set_service_line_adjudication_loop(
    context: X12ParserContext, segment_data: Dict
) -> None:
    """
    Sets service line adjudication loop 2430

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    service_line = _get_service_line(context)

    if TransactionLoops.CLAIM_SERVICE_LINE_LINE_ADJUDICATION_INFORMATION:
        service_line[
            TransactionLoops.CLAIM_SERVICE_LINE_LINE_ADJUDICATION_INFORMATION
        ] = []

    service_line[
        TransactionLoops.CLAIM_SERVICE_LINE_LINE_ADJUDICATION_INFORMATION
    ].append(
        {
            "cas_segment": [],
        }
    )

    adjudication_loop = service_line[
        TransactionLoops.CLAIM_SERVICE_LINE_LINE_ADJUDICATION_INFORMATION
    ][-1]
    context.set_loop_context(
        TransactionLoops.CLAIM_SERVICE_LINE_LINE_ADJUDICATION_INFORMATION,
        adjudication_loop,
    )


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
