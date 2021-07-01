"""
parse.py

Defines the classes and functions used to parse X12 270 005010X279A1 segments into a transactional model.
"""
from enum import Enum

from x12.models import X12SegmentGroup
from x12.parsing import X12SegmentParser, match

from .transaction_set import EligibilityInquiry


class EligibilityInquiryLoops(str, Enum):
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


class EligibilityInquiryParser(X12SegmentParser):
    """
    The 270 005010X279A1 parser.
    """

    def __init__(self):
        """
        Configures the data record for the 270 transaction.
        """
        super().__init__()
        self._data_record[EligibilityInquiryLoops.INFORMATION_SOURCE] = []

    def reset(self):
        """
        Resets the data record for the 270 transaction.
        """
        self._data_record[EligibilityInquiryLoops.INFORMATION_SOURCE] = []

    def load_model(self) -> X12SegmentGroup:
        """
        Loads the data model for the 280 transaction
        """
        return EligibilityInquiry(**self._data_record)


@match("ST")
def parse_st_segment(segment_data, context, data_record):
    context["current_loop"] = EligibilityInquiryLoops.HEADER
    data_record[EligibilityInquiryLoops.HEADER]["st_segment"] = segment_data


@match("BHT")
def parse_bht_segment(segment_data, context, data_record):
    data_record[EligibilityInquiryLoops.HEADER]["bht_segment"] = segment_data


@match("HL", conditions={"hierarchical_level_code": "20"})
def parse_information_source_hl_segment(segment_data, context, data_record):
    context["current_loop"] = EligibilityInquiryLoops.INFORMATION_SOURCE

    data_record[EligibilityInquiryLoops.INFORMATION_SOURCE].append(
        {"hl_segment": segment_data}
    )
    # TODO: record complete


@match("NM1")
def parse_nm1_segment(segment_data, context, data_record):
    if context["current_loop"] == EligibilityInquiryLoops.INFORMATION_SOURCE:
        context["current_loop"] = EligibilityInquiryLoops.INFORMATION_SOURCE_NAME

    if context["current_loop"] == EligibilityInquiryLoops.INFORMATION_SOURCE_NAME:
        information_source = data_record[EligibilityInquiryLoops.INFORMATION_SOURCE][-1]
        information_source[EligibilityInquiryLoops.INFORMATION_SOURCE_NAME] = {
            "nm1_segment": segment_data
        }


@match("SE")
def parse_se_segment(segment_data, context, data_record):
    context["current_loop"] = EligibilityInquiryLoops.FOOTER
    data_record[EligibilityInquiryLoops.FOOTER] = {"se_segment": segment_data}

    context["is_record_complete"] = True
