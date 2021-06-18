"""
test_complete_270.py


"""
import pytest
from x12.io import X12SegmentReader


@pytest.fixture
def raw_x12_data():
    return "\n".join(
        [
            "ISA*03*9876543210*01*9876543210*30*000000005      *30*12345          *131031*1147*^*00501*000000907*1*T*:~",
            "GS*HS*000000005*54321*20131031*1147*1*X*005010X279A1~",
            "ST*270*0001*005010X279A1~",
            "BHT*0022*13*10001234*20131031*1147~",
            "SE*1*0001~",
            "GE*1*1~",
            "IEA*1*000000907~",
        ]
    )


def test_x12_segment_reader(raw_x12_data):
    x12_segment_reader: X12SegmentReader = X12SegmentReader(raw_x12_data)
