"""
Tests use-cases for the 270 005010X279A1 (Eligibility Inquiry) transaction
"""

from x12.io import X12ModelReader
import pytest
from tests.support import assert_eq_model


@pytest.fixture
def x12_270_subscriber() -> str:
    return "\n".join(
        [
            "ISA*03*9876543210*01*9876543210*30*000000005      *30*12345          *131031*1147*^*00501*000000907*1*T*:~",
            "GS*HS*000000005*54321*20131031*1147*1*X*005010X279A1~",
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
            "N3*1400 ANYHOO LANE*APT 270~",
            "N4*SPARTANBURG*SC*29302~",
            "PRV*PC*HPI*3435612668~",
            "DMG*D8*19700101~",
            "INS*Y*18***************3~",
            "HI*BK:8901*BF:87200*BF:559~",
            "DTP*291*D8*20131031~",
            "EQ*30~",
            "AMT*R*37.50~",
            "AMT*PB*37.50~",
            "III*ZZ*21~",
            "REF*9F*660415~",
            "DTP*291*D8*20131031~",
            "SE*27*0001~",
            "GE*1*1~",
            "IEA*1*000000907~",
        ]
    )


@pytest.fixture
def x12_270_dependent() -> str:
    return "\n".join(
        [
            "ISA*03*9876543210*01*9876543210*30*000000005      *30*12345          *131031*1147*^*00501*000000907*1*T*:~",
            "GS*HS*000000005*54321*20131031*1147*1*X*005010X279A1~",
            "ST*270*0001*005010X279A1~",
            "BHT*0022*13*10001234*20131031*1147~",
            "HL*1**20*1~",
            "NM1*PR*2*PAYER C*****PI*12345~",
            "HL*2*1*21*1~",
            "NM1*1P*1*DOE*JOHN****XX*1467857193~",
            "REF*4A*000111222~",
            "N3*123 MAIN ST.*SUITE 42~",
            "N4*SAN MATEO*CA*94401~",
            "HL*3*2*22*1~",
            "NM1*IL*1******MI*00000000001~",
            "HL*4*3*23*0~",
            "TRN*1*930000000000*9800000004*PD~",
            "NM1*03*1*DOE*JANE~",
            "REF*6P*0123456789~",
            "N3*1400 ANYHOO LANE*APT 270~",
            "N4*SPARTANBURG*SC*29302~",
            "PRV*PC*HPI*3435612668~",
            "DMG*D8*19700101~",
            "INS*N*01~",
            "HI*BK:8901*BF:87200*BF:559~",
            "DTP*291*D8*20131031~",
            "EQ*30~",
            "SE*24*0001~",
            "GE*1*1~",
            "IEA*1*000000907~",
        ]
    )


@pytest.mark.parametrize("test_input", ["x12_270_subscriber", "x12_270_dependent"])
def test_270_model(request, test_input: str):
    input_value = request.getfixturevalue(test_input)
    assert_eq_model(input_value)


def test_270_properties_subscriber_use_case(x12_270_subscriber):
    """
    Tests the Eligibility Inquiry property accessors with the subscriber use-case.
    The subscriber use-case does not include a dependent record.
    The input data fixture reflects conventional Eligibility usage where a transaction contains a single
    information receiver, information source, subscriber, and optionally dependent.
    """

    with X12ModelReader(x12_270_subscriber) as r:
        transaction_model = [m for m in r.models()][0]

        information_source = transaction_model.information_source
        assert isinstance(information_source, dict)
        assert len(information_source) == 2
        assert "hl_segment" in information_source
        assert "loop_2100a" in information_source

        information_receiver = transaction_model.information_receiver
        assert isinstance(information_receiver, dict)
        assert len(information_receiver) == 2
        assert "hl_segment" in information_receiver
        assert "loop_2100b" in information_receiver

        subscriber = transaction_model.subscriber
        assert isinstance(subscriber, dict)
        assert len(subscriber) == 3
        assert "hl_segment" in subscriber
        assert "trn_segment" in subscriber
        assert "loop_2100c" in subscriber

        dependent = transaction_model.dependent
        assert dependent is None


def test_270_properties_dependent_use_case(x12_270_dependent):
    """
    Tests the Eligibility Inquiry property accessors with the dependent use-case.
    The dependent use-case exercises all available properties.
    The input data fixture reflects conventional Eligibility usage where a transaction contains a single
    information receiver, information source, subscriber, and optionally dependent.
    """

    with X12ModelReader(x12_270_dependent) as r:
        transaction_model = [m for m in r.models()][0]

        information_source = transaction_model.information_source
        assert len(information_source) == 2
        assert "hl_segment" in information_source
        assert "loop_2100a" in information_source

        information_receiver = transaction_model.information_receiver
        assert len(information_receiver) == 2
        assert "hl_segment" in information_receiver
        assert "loop_2100b" in information_receiver

        subscriber = transaction_model.subscriber
        assert len(subscriber) == 3
        assert "hl_segment" in subscriber
        assert "trn_segment" in subscriber
        assert "loop_2100c" in subscriber

        dependent = transaction_model.dependent
        assert len(dependent) == 3
        assert "hl_segment" in dependent
        assert "trn_segment" in dependent
        assert "loop_2100d" in dependent
