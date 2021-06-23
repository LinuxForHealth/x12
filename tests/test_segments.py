"""
test_segments.py

Tests the Pydantic X12 segment models
"""
from x12.segments import *


def test_bht_segment(x12_delimiters):
    segment_data = {
        "delimiters": x12_delimiters.dict(),
        "segment_name": "BHT",
        "structure_code": "0022",
        "purpose_code": "01",
        "transactional_identifier": "1c257041a955432091b0c073d788d29a",
        "transaction_creation_date": datetime.date(1998, 1, 1),
        "transaction_creation_time": datetime.time(hour=14, minute=0),
        "transaction_code": "RT",
    }

    bht_segment: BhtSegment = BhtSegment(**segment_data)
    assert bht_segment.dict() == segment_data


def test_ge_segment(x12_delimiters):
    segment_data = {
        "delimiters": x12_delimiters.dict(),
        "segment_name": "GE",
        "transaction_count": 1,
        "control_number": "1",
    }

    ge_segment: GeSegment = GeSegment(**segment_data)
    assert ge_segment.dict() == segment_data


def test_gs_segment(x12_delimiters):
    segment_data = {
        "delimiters": x12_delimiters.dict(),
        "segment_name": "GS",
        "id_code": "HS",
        "sender_code": "000000005",
        "receiver_code": "54321",
        "creation_date": datetime.date(2013, 10, 31),
        "creation_time": datetime.time(hour=11, minute=47),
        "control_number": "1",
        "responsible_agency_code": "X",
        "version_code": "005010X279A",
    }

    gs_segment: GsSegment = GsSegment(**segment_data)
    assert gs_segment.dict() == segment_data


def test_hl_segment(x12_delimiters):
    segment_data = {
        "delimiters": x12_delimiters.dict(),
        "segment_name": "HL",
        "id_number": 3,
        "parent_id_number": 2,
        "level_code": 22,
        "child_code": 0,
    }

    hl_segment: HlSegment = HlSegment(**segment_data)
    assert hl_segment.dict() == segment_data


def test_iea_segment(x12_delimiters):
    segment_data = {
        "delimiters": x12_delimiters.dict(),
        "segment_name": "IEA",
        "group_count": 1,
        "control_number": "000000907",
    }

    iea_segment: IeaSegment = IeaSegment(**segment_data)
    assert iea_segment.dict() == segment_data


def test_isa_segment(x12_delimiters):
    segment_data = {
        "delimiters": x12_delimiters.dict(),
        "segment_name": "ISA",
        "auth_qualifier": "03",
        "auth_information": "9876543210",
        "security_qualifier": "01",
        "security_information": "9876543210",
        "sender_qualifier": "30",
        "sender_id": "000000005      ",
        "receiver_qualifier": "30",
        "receiver_id": "12345          ",
        "interchange_date": datetime.date(2013, 10, 31),
        "interchange_time": datetime.time(11, 47),
        "repetition_separator": "^",
        "control_version": "00501",
        "control_number": "000000907",
        "acknowledgment_requested": "1",
        "interchange_usage": "T",
    }

    isa_segment: IsaSegment = IsaSegment(**segment_data)
    assert isa_segment.dict() == segment_data


def test_nm1_segment(x12_delimiters):
    segment_data = {
        "delimiters": x12_delimiters.dict(),
        "segment_name": "NM1",
        "entity_identifier_code": "PR",
        "entity_type_qualifier": 2,
        "name_last_org_name": "ACME",
        "code_qualifier": "PI",
        "identification_code": "12345",
    }
    nm1_segment: Nm1Segment = Nm1Segment(**segment_data)
    assert nm1_segment.dict(exclude_unset=True) == segment_data


def test_se_segment(x12_delimiters):
    segment_data = {
        "delimiters": x12_delimiters.dict(),
        "segment_name": "SE",
        "segment_count": 17,
        "control_number": "0001",
    }

    se_segment: SeSegment = SeSegment(**segment_data)
    assert se_segment.dict() == segment_data


def test_st_segment(x12_delimiters):
    segment_data = {
        "delimiters": x12_delimiters.dict(),
        "segment_name": "ST",
        "id": "270",
        "control_number": "0001",
        "reference_version": "005010X279A1",
    }

    st_segment: StSegment = StSegment(**segment_data)
    assert st_segment.dict() == segment_data
