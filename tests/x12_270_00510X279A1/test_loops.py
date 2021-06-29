"""
test_loops.py

Tests the loops modeled for the 270 00510X279A1 transaction
"""
import datetime

from x12.transactions.x12_270_005010X279A1.loops import Header, Loop2000A


def test_header_loop(x12_delimiters):
    loop_data = {
        "type": "LOOP",
        "name": "HEADER",
        "description": "270 Transaction Set Header",
        "st_segment": {
            "delimiters": x12_delimiters.dict(),
            "segment_name": "ST",
            "transaction_set_identifier_code": "270",
            "transaction_set_control_number": "0001",
            "implementation_convention_reference": "005010X279A1",
        },
        "bht_segment": {
            "delimiters": x12_delimiters.dict(),
            "segment_name": "BHT",
            "hierarchical_structure_code": "0022",
            "transaction_set_purpose_code": "01",
            "submitter_transactional_identifier": "1c257041a955432091b0c073d788d29a",
            "transaction_set_creation_date": datetime.date(1998, 1, 1),
            "transaction_set_creation_time": datetime.time(hour=14, minute=0),
        },
    }

    header: Header = Header(**loop_data)
    assert header.x12() == (
        "ST*270*0001*005010X279A1~\n"
        + "BHT*0022*01*1c257041a955432091b0c073d788d29a*19980101*140000~"
    )


def test_loop_2000a(x12_delimiters):
    loop_data = {
        "type": "LOOP",
        "name": "Loop2000A",
        "description": "Information Source",
        "hl_segment": {
            "delimiters": x12_delimiters,
            "segment_name": "HL",
            "hierarchical_id_number": "1",
            "hierarchical_level_code": "20",
            "hierarchical_child_code": "1",
        },
        "loop_2100a": {
            "type": "LOOP",
            "name": "Loop2100A",
            "description": "Information Source Name",
            "nm1_segment": {
                "segment_name": "NM1",
                "entity_identifier_code": "PR",
                "entity_type_qualifier": "2",
                "name_last_or_organization_name": "PAYER C",
                "identification_code_qualifier": "PI",
                "identification_code": "12345",
            },
        },
    }

    loop_2000a: Loop2000A = Loop2000A(**loop_data)
    assert loop_2000a.x12() == ("HL*1**20*1~\n" + "NM1*PR*2*PAYER C*****PI*12345~")
