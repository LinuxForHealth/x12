"""
test_segments.py

Tests 270 005010X279A1 segment implementations
"""
import datetime

from x12.transactions.x12_270_005010X279A1.segments import (
    HeaderBhtSegment,
    HeaderStSegment,
    Loop2000AHlSegment,
    Loop2100ANm1Segment,
)


def test_header_st_segment(x12_delimiters):
    segment_data = {
        "segment_name": "ST",
        "transaction_set_identifier_code": "270",
        "transaction_set_control_number": "0001",
        "implementation_convention_reference": "005010X279A1",
    }
    st_segment: HeaderStSegment = HeaderStSegment(**segment_data)
    assert st_segment.x12() == "ST*270*0001*005010X279A1~"


def test_header_bht_segment(x12_delimiters):
    segment_data = {
        "segment_name": "BHT",
        "hierarchical_structure_code": "0022",
        "transaction_set_purpose_code": "13",
        "submitter_transactional_identifier": "10001234",
        "transaction_set_creation_date": datetime.date(2013, 10, 31),
        "transaction_set_creation_time": datetime.time(11, 47),
    }
    bht_segment: HeaderBhtSegment = HeaderBhtSegment(**segment_data)
    assert bht_segment.x12() == "BHT*0022*13*10001234*20131031*114700~"


def test_loop_2000a_hl_segment():
    segment_data = {
        "segment_name": "HL",
        "hierarchical_id_number": "1",
        "hierarchical_level_code": "20",
        "hierarchical_child_code": "1",
    }
    hl_segment: Loop2000AHlSegment = Loop2000AHlSegment(**segment_data)
    assert hl_segment.x12() == "HL*1**20*1~"


def test_loop_2100a_nm1_segment():
    segment_data = {
        "segment_name": "NM1",
        "entity_identifier_code": "PR",
        "entity_type_qualifier": "2",
        "name_last_or_organization_name": "PAYER C",
        "identification_code_qualifier": "PI",
        "identification_code": "12345",
    }
    nm1_segment: Loop2100ANm1Segment = Loop2100ANm1Segment(**segment_data)
    assert nm1_segment.x12() == "NM1*PR*2*PAYER C*****PI*12345~"
