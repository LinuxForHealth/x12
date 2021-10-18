"""
test_837_005010XX222A2.py
"""
from x12.io import X12ModelReader
import pytest
from tests.support import assert_eq_model


@pytest.fixture()
def x12_837_commercial_health_insurance() -> str:
    """
    Example 1 - Commercial Health Insurance from the 837 005010XX222A2 specification.
    Patient is not the subscriber.
    """
    return "\n".join(
        [
            "ISA*03*9876543210*01*9876543210*30*000000005      *30*12345          *131031*1147*^*00501*000000907*1*T*:~",
            "GS*HC*000000005*54321*20131031*1147*1*X*005010X222A2~",
            "ST*837*0021*005010X222A2~",
            "BHT*0019*00*244579*20061015*1023*CH~",
            "NM1*41*2*PREMIER BILLING SERVICE*****46*TGJ23~",
            "PER*IC*JERRY*TE*3055552222*EX*231~",
            "NM1*40*2*KEY INSURANCE COMPANY*****46*66783JJT~",
            "HL*1**20*1~",
            "PRV*BI*PXC*203BF0100Y~",
            "NM1*85*2*BEN KILDARE SERVICE*****XX*1912301953~",
            "N3*234 SEAWAY ST~",
            "N4*MIAMI*FL*331110000~",
            "REF*EI*587654321~",
            "NM1*87*2~",
            "N3*2345 OCEAN BLVD~",
            "N4*MIAMI*FL*33111~",
            "HL*2*1*22*1~",
            "SBR*P**2222-SJ******CI~",
            "NM1*IL*1*SMITH*JANE****MI*JS00111223333~",
            "NM1*PR*2*KEY INSURANCE COMPANY*****PI*999996666~",
            "HL*3*2*23*0~",
            "PAT*19~",
            "NM1*QC*1*SMITH*TED~",
            "N3*236 N MAIN ST~",
            "N4*MIAMI*FL*33413~",
            "DMG*D8*19730501*M~",
            "CLM*26463774*100.00***11:B:1*Y*A*Y*I~",
            "REF*D9*17312345600006351~",
            "HI*BK:0340*BF:V7389~",
            "LX*1~",
            "SV1*HC:99213*40.00*UN*1.00***1~",
            "DTP*472*D8*20061003~",
            "LX*2~",
            "SV1*HC:87070*15.00*UN*1.00***1~",
            "DTP*472*D8*20061003~",
            "LX*3~",
            "SV1*HC:99214*35.00*UN*1.00***2~",
            "DTP*472*D8*20061010~",
            "LX*4~",
            "SV1*HC:86663*10.00*UN*1.00***2~",
            "DTP*472*D8*20061010~",
            "SE*40*0021~",
            "GE*1*1~",
            "IEA*1*000000907~",
        ]
    )


@pytest.fixture()
def x12_837_drug_in_office() -> str:
    """
    Drug Example 1 - from the 837 005010XX222A2 specification.
    Patient is the subscriber.
    """
    return "\n".join(
        [
            "ISA*03*9876543210*01*9876543210*30*000000005      *30*12345          *131031*1147*^*00501*000000907*1*T*:~",
            "GS*HC*000000005*54321*20131031*1147*1*X*005010X222A2~",
            "ST*837*0711*005010X222A2~",
            "BHT*0019*00*0013*20040801*1200*CH~",
            "NM1*41*2*ASSOCIATES IN MEDICINE*****46*587654321~",
            "PER*IC*BUD HOLLY*TE*8017268899~",
            "NM1*40*2*XYZ RECEIVER*****46*369852758~",
            "HL*1**20*1~",
            "NM1*85*2*ASSOCIATES IN MEDICINE*****XX*1234567893~",
            "N3*1313 LAS VEGAS BOULEVARD~",
            "N4*LAS VEGAS*NV*89109~",
            "REF*EI*587654321~",
            "HL*2*1*22*0~",
            "SBR*P*18*GRP01020102******CI~",
            "NM1*IL*1*VAUGHN*STEVE*R***MI*MBRID12345~",
            "N3*236 DIAMOND ST~",
            "N4*LAS VEGAS*NV*89109~",
            "DMG*D8*19430501*M~",
            "NM1*PR*2*R&R HEALTH PLAN*****XV*PLANID12345~",
            "CLM*CLMNO12345*103.37***11:B:1*Y*A*Y*Y~",
            "HI*BK:03591~",
            "NM1*82*1*HENDRIX*JIM****XX*1122333341~",
            "PRV*PE*PXC*208D00000X~",
            "LX*1~",
            "SV1*HC:90782*50.00*UN*1.00*11**1~",
            "DTP*472*D8*20040711~",
            "LX*2~",
            "SV1*HC:J1550*53.37*UN*1.00*11**1~",
            "DTP*472*D8*20040711~",
            "AMT*T*3.37~",
            "LIN**N4*00026063512~",
            "CTP****10.00*ML~",
            "SE*31*0711~",
            "GE*1*1~",
            "IEA*1*000000907~",
        ]
    )


@pytest.mark.parametrize(
    "test_input", ["x12_837_commercial_health_insurance", "x12_837_drug_in_office"]
)
def test_837_model(request, test_input: str):
    input_value = request.getfixturevalue(test_input)
    assert_eq_model(input_value)


def test_837_subscriber_properties(x12_837_drug_in_office):
    """
    Test 837 properties where the patient is the subscriber
    """
    with X12ModelReader(x12_837_drug_in_office) as r:
        model_result = [m for m in r.models()]
        assert len(model_result) == 1

        model = model_result[0]

        nm1_segment = model.patient["loop_2010ba"]["nm1_segment"]
        assert nm1_segment["name_last_or_organization_name"] == "VAUGHN"
        assert nm1_segment["name_first"] == "STEVE"

        claim_data = model.claim
        assert claim_data["clm_segment"] is not None
        assert len(claim_data["sv1_segment"]) == 2


def test_837_dependent_properties(x12_837_commercial_health_insurance):
    """
    Test 837 properties where the patient is not the subscriber
    """
    with X12ModelReader(x12_837_commercial_health_insurance) as r:
        model_result = [m for m in r.models()]
        assert len(model_result) == 1

        model = model_result[0]
        assert "loop_2300" not in model

        nm1_segment = model.patient["loop_2010ca"]["nm1_segment"]
        assert nm1_segment["name_last_or_organization_name"] == "SMITH"
        assert nm1_segment["name_first"] == "TED"

        claim_data = model.claim
        assert claim_data["clm_segment"] is not None
        assert len(claim_data["sv1_segment"]) == 4
