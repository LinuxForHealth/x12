"""
test_control_segments.py

Tests X12 Control Segment Models
"""
from x12.v5010.control_segments import *
import datetime


def test_isa_segment():
    fields = {
        "loop_context": {
            "id": "EDI_CONTROL",
            "description": "INTERCHANGE CONTROL SEGMENTS"
        },
        "segment_name": "ISA",
        "sender_id": "SENDER",
        "receiver_id": "RECEIVER",
        "interchange_date": datetime.date(year=2021,month=6,day=16),
        "interchange_time": datetime.time(hour=13, minute=10),
        "interchange_control_number": 512_987_762
    }

    isa_segment = IsaSegment(**fields)
    isa_x12 = isa_segment.x12()
    assert len(isa_x12) == 106
    assert isa_x12 == "ISA*00*          *  *          *ZZ*SENDER         *ZZ*RECEIVER       *210616*1310*^*00501*512987762*0*T*:~"
