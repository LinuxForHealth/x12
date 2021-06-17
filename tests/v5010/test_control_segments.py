"""
test_control_segments.py

Tests X12 Control Segment Models
"""
from x12.v5010.control_segments import *
import datetime


def test_isa_segment():
    fields = {
        "loop_context": {
            "id": "INTERCHANGE_HEADER",
            "description": "EDI MESSAGE INTERCHANGE HEADER SEGMENT",
        },
        "segment_name": "ISA",
        "sender_id": "SENDER",
        "receiver_id": "RECEIVER",
        "interchange_date": datetime.date(year=2021, month=6, day=16),
        "interchange_time": datetime.time(hour=13, minute=10),
        "interchange_control_number": 512_987_762,
    }

    isa_segment = IsaSegment(**fields)
    isa_x12 = isa_segment.x12()
    assert len(isa_x12) == 106
    assert (
        isa_x12
        == "ISA*00*          *  *          *ZZ*SENDER         *ZZ*RECEIVER       *210616*1310*^*00501*512987762*0*T*:~"
    )


def test_gs_segment():
    fields = {
        "loop_context": {
            "id": "FUNCTIONAL_HEADER",
            "description": "ASC X12 FUNCTIONAL GROUP HEADER SEGMENT",
        },
        "segment_name": "GS",
        "functional_id_code": "HS",
        "application_sender_code": "SENDER_CODE",
        "application_receiver_code": "RECEIVER_CODE",
        "creation_date": datetime.date(2021, 6, 16),
        "creation_time": datetime.time(13, 10),
        "group_control_number": 1,
    }
    gs_segment = GsSegment(**fields)
    assert (
        gs_segment.x12()
        == "GS*HS*SENDER_CODE*RECEIVER_CODE*20210616*1310*1*X*005010X279A1~"
    )


def test_ge_segment():
    fields = {
        "loop_context": {
            "id": "FUNCTIONAL_FOOTER",
            "description": "ASC X12 FUNCTIONAL GROUP FOOTER SEGMENT",
        },
        "segment_name": "GE",
        "transaction_set_count": 1,
        "group_control_number": 1,
    }
    ge_segment = GeSegment(**fields)
    assert ge_segment.x12() == "GE*1*1~"


def test_iea_segment():
    fields = {
        "loop_context": {
            "id": "INTERCHANGE_FOOTER",
            "description": "EDI MESSAGE INTERCHANGE FOOTER SEGMENT",
        },
        "segment_name": "IEA",
        "functional_group_count": 1,
        "interchange_control_number": 512_987_762,
    }

    iea_segment = IeaSegment(**fields)
    assert iea_segment.x12() == "IEA*1*512987762~"
