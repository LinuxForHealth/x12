"""
parsing.py

Parses X12 835 005010X221A1 segments into a transactional domain model.

The parsing module includes a specific parser for the 835 transaction and loop parsing functions to create new loops
as segments are streamed to the transactional data model.

Loop parsing functions are implemented as set_[description]_loop(context: X12ParserContext, segment_data: Dict).
"""
from enum import Enum
from linuxforhealth.x12.parsing import X12ParserContext, match
from typing import Dict


class TransactionLoops(str, Enum):
    """
    The loops used to support the 835 005010X221A1 format.
    """

    HEADER = "header"
    PAYER_IDENTIFICATION = "loop_1000a"
    PAYEE_IDENTIFICATION = "loop_1000b"
    CLAIM_PAYMENT_LINE_ITEM = "loop_2000"
    CLAIM_PAYMENT_INFORMATION = "loop_2100"
    SERVICE_PAYMENT_INFORMATION = "loop_2110"
    FOOTER = "footer"


def _get_header(context: X12ParserContext) -> Dict:
    """Returns the 837 transaction header"""
    return context.transaction_data[TransactionLoops.HEADER]


def _get_claim_payment_line(context: X12ParserContext) -> Dict:
    """Returns the current claim payment line record"""
    return context.transaction_data[TransactionLoops.CLAIM_PAYMENT_LINE_ITEM][-1]


def _get_claim_payment_information(context: X12ParserContext) -> Dict:
    """Returns the current claim payment info"""
    claim_payment_line = _get_claim_payment_line(context)
    return claim_payment_line[TransactionLoops.CLAIM_PAYMENT_INFORMATION][-1]


@match("ST")
def set_header_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the transaction set header loop for the 835 transaction set.

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    context.transaction_data[TransactionLoops.HEADER] = {"ref_segment": []}
    header = context.transaction_data[TransactionLoops.HEADER]
    context.set_loop_context(TransactionLoops.HEADER, header)


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


@match("N1", conditions={"entity_identifier_code": "PE"})
def set_payee_identification_loop(
    context: X12ParserContext, segment_data: Dict
) -> None:
    """
    Sets the payee identification loop

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    context.transaction_data[TransactionLoops.PAYEE_IDENTIFICATION] = {
        "ref_segment": []
    }
    loop_data = context.transaction_data[TransactionLoops.PAYEE_IDENTIFICATION]
    context.set_loop_context(TransactionLoops.PAYEE_IDENTIFICATION, loop_data)


@match("LX")
def set_claim_payment_line_item_loop(
    context: X12ParserContext, segment_data: Dict
) -> None:
    """
    Sets the header number loop

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    if TransactionLoops.CLAIM_PAYMENT_LINE_ITEM not in context.transaction_data:
        context.transaction_data[TransactionLoops.CLAIM_PAYMENT_LINE_ITEM] = [{}]
    else:
        context.transaction_data[TransactionLoops.CLAIM_PAYMENT_LINE_ITEM].append({})

    loop_data = context.transaction_data[TransactionLoops.CLAIM_PAYMENT_LINE_ITEM][-1]
    context.set_loop_context(TransactionLoops.CLAIM_PAYMENT_LINE_ITEM, loop_data)


@match("CLP")
def set_claim_payment_information_loop(
    context: X12ParserContext, segment_data: Dict
) -> None:
    """
    Sets the claim payment loop

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """
    claim_payment_line = _get_claim_payment_line(context)

    if TransactionLoops.CLAIM_PAYMENT_INFORMATION not in claim_payment_line:
        claim_payment_line[TransactionLoops.CLAIM_PAYMENT_INFORMATION] = []

    claim_payment_line[TransactionLoops.CLAIM_PAYMENT_INFORMATION].append(
        {
            "cas_segment": [],
            "nm1_segment": [],
            "ref_segment": [],
            "dtm_segment": [],
            "per_segment": [],
            "amt_segment": [],
            "qty_segment": [],
        }
    )

    loop_data = claim_payment_line[TransactionLoops.CLAIM_PAYMENT_INFORMATION][-1]
    context.set_loop_context(TransactionLoops.CLAIM_PAYMENT_INFORMATION, loop_data)


@match("SVC")
def set_service_payment_information_loop(
    context: X12ParserContext, segment_data: Dict
) -> None:
    """
    Sets the service payment information loop
    """
    claim_payment_information = _get_claim_payment_information(context)

    if TransactionLoops.SERVICE_PAYMENT_INFORMATION not in claim_payment_information:
        claim_payment_information[TransactionLoops.SERVICE_PAYMENT_INFORMATION] = []

    claim_payment_information[TransactionLoops.SERVICE_PAYMENT_INFORMATION].append(
        {
            "dtm_segment": [],
            "cas_segment": [],
            "ref_segment": [],
            "amt_segment": [],
            "qty_segment": [],
            "lq_segment": [],
        }
    )

    loop_data = claim_payment_information[TransactionLoops.SERVICE_PAYMENT_INFORMATION][
        -1
    ]
    context.set_loop_context(TransactionLoops.SERVICE_PAYMENT_INFORMATION, loop_data)


@match("PLB")
def set_plb_footer_loop(context: X12ParserContext, segment_data: Dict) -> None:
    """
    Sets the transaction set footer loop if the PLB optional segment is encountered.

    :param context: The X12Parsing context which contains the current loop and transaction record.
    :param segment_data: The current segment data
    """

    context.set_loop_context(
        TransactionLoops.FOOTER, context.transaction_data["footer"]
    )


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
