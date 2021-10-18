"""
test_835_005010XX221A1.py
"""
from x12.io import X12ModelReader
import pytest
from tests.support import assert_eq_model


@pytest.fixture
def x12_835_managed_care() -> str:
    """
    Example 2, Managed Care Environment, from the 835 005010XX221A1 specification.
    Within the managed care environment, dollars and data are sent separately (billing and provider).
    """
    return "\n".join(
        [
            "ISA*03*9876543210*01*9876543210*30*000000005      *30*12345          *131031*1147*^*00501*000000907*1*T*:~",
            "GS*HP*000000005*54321*20131031*1147*1*X*005010X221A1~",
            "ST*835*112233~",
            "BPR*I*945.00*C*ACH*CCP*01*888999777*DA*24681012*1935665544**01*111333555*DA*144444*20002316~",
            "TRN*1*7170066655*1935665544~",
            "DTM*405*20020314~",
            "N1*PR*RUSHMORE LIFE~",
            "N3*10 SOUTH AVENUE~",
            "N4*RAPID CITY*SD*55111~",
            "N1*PE*ACME MEDICAL CENTER*XX*5544667733~",
            "REF*TJ*777667755~",
            "LX*1~",
            "CLP*5554555444*1*800.00*450.00*300.00*12*94060555410000~",
            "CAS*CO*A2*50.00~",
            "NM1*QC*1*BUDD*WILLIAM****MI*33344555510~",
            "SVC*HC:99211*800.00*500.00~",
            "DTM*150*20020301~",
            "DTM*151*20020304~",
            "CAS*PR*1*300.00~",
            "CLP*8765432112*1*1200.00*495.00*600.00*12*94077799230000~",
            "CAS*CO*A2*55.00~",
            "NM1*QC*1*SETTLE*SUSAN****MI*44455666610~",
            "SVC*HC:93555*1200.00*550.00~",
            "DTM*150*20020310~",
            "DTM*151*20020312~",
            "CAS*PR*1*600.00~",
            "CAS*CO*45*50.00~",
            "SE*26*112233~",
            "GE*1*1~",
            "IEA*1*000000907~",
        ]
    )


@pytest.mark.parametrize("test_input", ["x12_835_managed_care"])
def test_835_model(request, test_input: str):
    input_value = request.getfixturevalue(test_input)
    assert_eq_model(input_value)


def test_835_properties(x12_835_managed_care):
    """
    Test 835 properties
    """
    with X12ModelReader(x12_835_managed_care) as r:
        model_result = [m for m in r.models()]
        assert len(model_result) == 1

        model = model_result[0]

        n1_segment = model.payer["n1_segment"]
        assert n1_segment["name"] == "RUSHMORE LIFE"

        n1_segment = model.payee["n1_segment"]
        assert n1_segment["name"] == "ACME MEDICAL CENTER"

        claim_data = model.claim
        assert "clp_segment" in claim_data
        assert "cas_segment" in claim_data
        assert "loop_2110" in claim_data
