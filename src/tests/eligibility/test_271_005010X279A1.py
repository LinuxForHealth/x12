"""
Tests use-cases for the 271 005010X279A1 (Eligibility Benefit Response) transaction
"""
from x12.io import X12ModelReader
import pytest
from tests.support import assert_eq_model


@pytest.fixture
def x12_271_subscriber() -> str:
    return "\n".join(
        [
            "ISA*03*9876543210*01*9876543210*30*000000005      *30*12345          *131031*1147*^*00501*000000907*1*T*:~",
            "GS*HB*000000005*54321*20131031*1147*1*X*005010X279A1~",
            "ST*271*0001*005010X279A1~",
            "BHT*0022*11*10001234*20131031*1147~",
            "HL*1**20*1~",
            "NM1*PR*2*PAYER C*****PI*12345~",
            "HL*2*1*21*1~",
            "NM1*1P*1*DOE*JOHN****XX*1467857193~",
            "PRV*RF*PXC*207Q00000X~",
            "HL*3*2*22*0~",
            "TRN*2*930000000000*9800000004~",
            "NM1*IL*1*DOE*JOHN****MI*00000000001~",
            "N3*1500 ANYHOO AVENUE*APT 215~",
            "N4*SAN MATEO*CA*94401~",
            "DMG*D8*19700101*M~",
            "DTP*346*D8*20210101~",
            "EB*1**30**GOLD 123 PLAN~",
            "EB*L~",
            "LS*2120~",
            "NM1*1P*1*DOE*JOHN****XX*1467857193~",
            "LE*2120~",
            "EB*1**1^33^35^47^86^88^98^AL^MH^UC~",
            "EB*B**1^33^35^47^86^88^98^AL^MH^UC*HM*GOLD 123 PLAN*27*10.00*****Y~",
            "EB*B**1^33^35^47^86^88^98^AL^MH^UC*HM*GOLD 123 PLAN*27*30.00*****N~",
            "SE*23*0001~",
            "GE*1*1~",
            "IEA*1*000000907~",
        ]
    )


@pytest.fixture
def x12_271_dependent() -> str:
    return "\n".join(
        [
            "ISA*03*9876543210*01*9876543210*30*000000005      *30*12345          *131031*1147*^*00501*000000907*1*T*:~",
            "GS*HB*000000005*54321*20131031*1147*1*X*005010X279A1~",
            "ST*271*0001*005010X279A1~",
            "BHT*0022*11*10001234*20131031*1147~",
            "HL*1**20*1~",
            "NM1*PR*2*PAYER C*****PI*12345~",
            "HL*2*1*21*1~",
            "NM1*1P*1*DOE*JOHN****XX*1467857193~",
            "PRV*RF*PXC*207Q00000X~",
            "HL*3*2*22*1~",
            "NM1*IL*1*DOE*JAMES****MI*00000000001~",
            "N3*1500 ANYHOO AVENUE*APT 215~",
            "N4*SAN MATEO*CA*94401~",
            "DMG*D8*19700101*M~",
            "HL*4*3*23*0~",
            "TRN*2*930000000000*9800000004~",
            "NM1*IL*1*DOE*JAMES****MI*00000000002~",
            "N3*1500 ANYHOO AVENUE*APT 215~",
            "N4*SAN MATEO*CA*94401~",
            "DMG*D8*20150101*M~",
            "DTP*346*D8*20210101~",
            "EB*1**30**GOLD 123 PLAN~",
            "EB*L~",
            "LS*2120~",
            "NM1*1P*1*DOE*JOHN****XX*1467857193~",
            "LE*2120~",
            "EB*1**1^33^35^47^86^88^98^AL^MH^UC~",
            "EB*B**1^33^35^47^86^88^98^AL^MH^UC*HM*GOLD 123 PLAN*27*10.00*****Y~",
            "EB*B**1^33^35^47^86^88^98^AL^MH^UC*HM*GOLD 123 PLAN*27*30.00*****N~",
            "SE*28*0001~",
            "GE*1*1~",
            "IEA*1*000000907~",
        ]
    )


@pytest.mark.parametrize("test_input", ["x12_271_subscriber", "x12_271_dependent"])
def test_271_model(request, test_input: str):
    input_value = request.getfixturevalue(test_input)
    assert_eq_model(input_value)


def test_271_properties_subscriber_use_case(x12_271_subscriber):
    """
    Tests the Eligibility Benefit property accessors with the subscriber use-case.
    The subscriber use-case does not include a dependent record.
    The input data fixture reflects conventional Eligibility usage where a transaction contains a single
    information receiver, information source, subscriber, and optionally dependent.
    """

    with X12ModelReader(x12_271_subscriber) as r:
        transaction_model = [m for m in r.models()][0]

        information_source = transaction_model.information_source
        assert isinstance(information_source, dict)
        assert len(information_source) == 3
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


def test_271_properties_dependent_use_case(x12_271_dependent):
    """
    Tests the Eligibility Benefit property accessors with the dependent use-case.
    The input data fixture reflects conventional Eligibility usage where a transaction contains a single
    information receiver, information source, subscriber, and optionally dependent.
    """

    with X12ModelReader(x12_271_dependent) as r:
        transaction_model = [m for m in r.models()][0]

        information_source = transaction_model.information_source
        assert isinstance(information_source, dict)
        assert len(information_source) == 3
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
        assert isinstance(dependent, dict)
        assert len(dependent) == 3
        assert "hl_segment" in dependent
        assert "trn_segment" in dependent
        assert "loop_2100d" in dependent
