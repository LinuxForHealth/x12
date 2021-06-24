"""
test_segments.py

Tests the Pydantic X12 segment models
"""
from x12.segments import *


def test_bht_segment(x12_delimiters):
    segment_data = {
        "delimiters": x12_delimiters.dict(),
        "segment_name": "BHT",
        "hierarchical_structure_code": "0022",
        "transaction_set_purpose_code": "01",
        "submitter_transactional_identifier": "1c257041a955432091b0c073d788d29a",
        "transaction_set_creation_date": datetime.date(1998, 1, 1),
        "transaction_set_creation_time": datetime.time(hour=14, minute=0),
        "transaction_type_code": "RT",
    }

    bht_segment: BhtSegment = BhtSegment(**segment_data)
    assert bht_segment.dict() == segment_data


def test_ge_segment(x12_delimiters):
    segment_data = {
        "delimiters": x12_delimiters.dict(),
        "segment_name": "GE",
        "number_of_transaction_sets_included": 1,
        "group_control_number": "1",
    }

    ge_segment: GeSegment = GeSegment(**segment_data)
    assert ge_segment.dict() == segment_data


def test_gs_segment(x12_delimiters):
    segment_data = {
        "delimiters": x12_delimiters.dict(),
        "segment_name": "GS",
        "functional_identifier_code": "HS",
        "application_sender_code": "000000005",
        "application_receiver_code": "54321",
        "functional_group_creation_date": datetime.date(2013, 10, 31),
        "functional_group_creation_time": datetime.time(hour=11, minute=47),
        "group_control_number": "1",
        "responsible_agency_code": "X",
        "version_identifier_code": "005010X279A",
    }

    gs_segment: GsSegment = GsSegment(**segment_data)
    assert gs_segment.dict() == segment_data


def test_hl_segment(x12_delimiters):
    segment_data = {
        "delimiters": x12_delimiters.dict(),
        "segment_name": "HL",
        "hierarchical_id_number": "3",
        "hierarchical_parent_id_number": "2",
        "hierarchical_level_code": "22",
        "hierarchical_child_code": "0",
    }

    hl_segment: HlSegment = HlSegment(**segment_data)
    assert hl_segment.dict() == segment_data


def test_iea_segment(x12_delimiters):
    segment_data = {
        "delimiters": x12_delimiters.dict(),
        "segment_name": "IEA",
        "number_of_included_functional_groups": 1,
        "interchange_control_number": "000000907",
    }

    iea_segment: IeaSegment = IeaSegment(**segment_data)
    assert iea_segment.dict() == segment_data


def test_isa_segment(x12_delimiters):
    segment_data = {
        "delimiters": x12_delimiters.dict(),
        "segment_name": "ISA",
        "authorization_information_qualifier": "03",
        "authorization_information": "9876543210",
        "security_information_qualifier": "01",
        "security_information": "9876543210",
        "interchange_sender_qualifier": "30",
        "interchange_sender_id": "000000005      ",
        "interchange_receiver_qualifier": "30",
        "interchange_receiver_id": "12345          ",
        "interchange_date": datetime.date(2013, 10, 31),
        "interchange_time": datetime.time(11, 47),
        "repetition_separator": "^",
        "interchange_control_version_number": "00501",
        "interchange_control_number": "000000907",
        "acknowledgment_requested": "1",
        "interchange_usage_indicator": "T",
    }

    isa_segment: IsaSegment = IsaSegment(**segment_data)
    assert isa_segment.dict() == segment_data


def test_nm1_segment(x12_delimiters):
    segment_data = {
        "delimiters": x12_delimiters.dict(),
        "segment_name": "NM1",
        "entity_identifier_code": "PR",
        "entity_type_qualifier": "2",
        "name_last_or_organization_name": "ACME",
        "identification_code_qualifier": "PI",
        "identification_code": "12345",
    }
    nm1_segment: Nm1Segment = Nm1Segment(**segment_data)
    assert nm1_segment.dict(exclude_unset=True) == segment_data


def test_se_segment(x12_delimiters):
    segment_data = {
        "delimiters": x12_delimiters.dict(),
        "segment_name": "SE",
        "transaction_segment_count": 17,
        "transaction_set_control_number": "0001",
    }

    se_segment: SeSegment = SeSegment(**segment_data)
    assert se_segment.dict() == segment_data


def test_st_segment(x12_delimiters):
    segment_data = {
        "delimiters": x12_delimiters.dict(),
        "segment_name": "ST",
        "transaction_set_identifier_code": "270",
        "transaction_set_control_number": "0001",
        "implementation_convention_reference": "005010X279A1",
    }

    st_segment: StSegment = StSegment(**segment_data)
    assert st_segment.dict() == segment_data
