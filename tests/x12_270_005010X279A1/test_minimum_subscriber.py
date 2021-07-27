"""
test_minimum_subscriber.py

Tests a 270 transaction containing minimum subscriber demographics.
"""

import pytest
from x12.io import X12ModelReader


@pytest.fixture
def x12_transaction():
    return "\n".join(
        [
            "ST*270*0001*005010X279A1~",
            "BHT*0022*13*10001234*20131031*1147~",
            "HL*1**20*1~",
            "NM1*PR*2*PAYER C*****PI*12345~",
            "HL*2*1*21*1~",
            "NM1*1P*1*DOE*JOHN****XX*1467857193~",
            "REF*4A*000111222~",
            "N3*123 MAIN ST.*SUITE 42~",
            "N4*SAN MATEO*CA*94401~",
            "HL*3*2*22*0~",
            "TRN*1*930000000000*9800000004*PD~",
            "NM1*IL*1*DOE*JOHN****MI*00000000001~",
            "REF*6P*0123456789~",
            "DMG*D8*19700101~",
            "DTP*291*D8*20131031~",
            "EQ*1~",
            "SE*17*0001~",
        ]
    )


@pytest.fixture
def x12_input(
    x12_270_control_header: str, x12_transaction: str, x12_270_control_footer: str
):
    return f"{x12_270_control_header}{x12_transaction}{x12_270_control_footer}"


def test_minimum_subscriber(x12_input, x12_transaction):
    with X12ModelReader(x12_input) as r:
        model_result = [m for m in r.models()]
        assert len(model_result) == 1
        assert model_result[0].x12() == x12_transaction
