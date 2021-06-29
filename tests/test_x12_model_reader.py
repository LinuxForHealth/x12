import pytest
from x12.io import X12ModelReader


@pytest.fixture()
def x12_sample():
    return "\n".join(
        [
            "ISA*03*9876543210*01*9876543210*30*000000005      *30*12345          *131031*1147*^*00501*000000907*1*T*:~",
            "GS*HS*000000005*54321*20131031*1147*1*X*005010X279A1~",
            "ST*270*0001*005010X279A1~",
            "BHT*0022*13*10001234*20131031*1147~",
            "HL*1**20*1~",
            "NM1*PR*2*PAYER C*****PI*12345~",
            "SE*17*0001~",
            "GE*1*1~",
            "IEA*1*000000907~",
        ]
    )


def test_model_reader(x12_sample):
    with X12ModelReader(x12_sample) as r:
        for m in r.model():
            print(m.__class__)
