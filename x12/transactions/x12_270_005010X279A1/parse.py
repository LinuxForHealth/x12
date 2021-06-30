from x12.parse import X12SegmentParser, match
from x12.models import X12SegmentGroup
from .transaction_set import EligibilityInquiry
from enum import Enum


class EligibilityInquiryLoops(str, Enum):
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
    def __init__(self):
        super().__init__()
        self._data_record[EligibilityInquiryLoops.INFORMATION_SOURCE] = []

    def load_model(self) -> X12SegmentGroup:
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
