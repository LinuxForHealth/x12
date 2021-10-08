"""
conftest.py

Pytest Global Fixtures
"""
import pytest

from x12.config import X12Config
from x12.models import X12Delimiters
from x12.parsing import X12ParserContext


@pytest.fixture
def simple_270_with_new_lines() -> str:
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
            "DMG*D8*19700101~",
            "DTP*291*D8*20131031~",
            "EQ*1~",
            "SE*17*0001~",
            "GE*1*1~",
            "IEA*1*000000907~",
        ]
    )


@pytest.fixture
def simple_270_one_line(simple_270_with_new_lines) -> str:
    return simple_270_with_new_lines.replace("\n", "")


@pytest.fixture
def large_x12_message() -> str:
    """
    Generates a large x12 message by repeating a transaction set a fixed number of times.
    :return: large x12 message
    """

    x12_message: str = "\n".join(
        [
            "ISA*03*9876543210*01*9876543210*30*000000005      *30*12345          *131031*1147*^*00501*000000907*1*T*:~",
            "GS*HS*000000005*54321*20131031*1147*1*X*005010X279A1~",
        ]
    )

    x12_message += "\n"
    # will create 5000 transaction sets with 17 models each
    for i in range(1, 5_001, 1):
        transaction_set = "\n".join(
            [
                # ST02 is the transaction set id - zero filled to 4 characters
                f"ST*270*{i:04d}*005010X279A1~",
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
                # SE02 is the transaction set id - zero filled to 4 characters
                f"SE*17*{i:04d}~",
            ]
        )
        x12_message += transaction_set + "\n"

    x12_message += "\n".join(["GE*1*1~", "IEA*1*000000907~"])

    return x12_message


@pytest.fixture
def config() -> X12Config:
    config: X12Config = X12Config()
    config.x12_reader_buffer_size = 1024000
    return config


@pytest.fixture
def x12_delimiters() -> X12Delimiters:
    return X12Delimiters()


@pytest.fixture
def x12_parser_context() -> X12ParserContext:
    return X12ParserContext()


@pytest.fixture
def x12_control_header() -> str:
    """
    Returns a general X12 control header containing ISA and GS segments.

    The version identifiers in GS01 and GS08 are placeholders, set to "GS01" and "Gs08", and should be set as
    appropriate within code that consumes this fixture.
    """
    return "\n".join(
        [
            "ISA*03*9876543210*01*9876543210*30*000000005      *30*12345          *131031*1147*^*00501*000000907*1*T*:~",
            "GS*GS01*000000005*54321*20131031*1147*1*X*GS08~\n",
        ]
    )


@pytest.fixture
def x12_control_footer() -> str:
    return "\n".join(
        [
            "GE*1*1~",
            "IEA*1*000000907~",
        ]
    )


@pytest.fixture
def x12_270_subscriber_transaction() -> str:
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
        ]
    )


@pytest.fixture
def x12_270_subscriber_input(
    x12_control_header, x12_270_subscriber_transaction, x12_control_footer
) -> str:
    x12_270_header: str = x12_control_header.replace("GS01", "HS").replace(
        "GS08", "005010X279A1"
    )
    return f"{x12_270_header}{x12_270_subscriber_transaction}{x12_control_footer}"


@pytest.fixture
def x12_270_dependent_transaction() -> str:
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
        ]
    )


@pytest.fixture
def x12_270_dependent_input(
    x12_control_header, x12_270_dependent_transaction, x12_control_footer
) -> str:
    x12_270_header: str = x12_control_header.replace("GS01", "HS").replace(
        "GS08", "005010X279A1"
    )

    return f"{x12_270_header}{x12_270_dependent_transaction}{x12_control_footer}"


@pytest.fixture
def x12_with_custom_delimiters() -> str:
    return "\n".join(
        [
            "ISA|03|9876543210|01|9876543210|30|000000005      |30|12345          |131031|1147|^|00501|000000907|1|T|:?",
            "GS|HS|000000005|54321|20131031|1147|1|X|005010X279A1?",
            "ST|270|0001|005010X279A1?",
            "BHT|0022|13|10001234|20131031|1147?",
            "HL|1||20|1?",
            "NM1|PR|2|PAYER C|||||PI|12345?",
            "HL|2|1|21|1?",
            "NM1|1P|1|DOE|JOHN||||XX|1467857193?",
            "REF|4A|000111222?",
            "N3|123 MAIN ST.|SUITE 42?",
            "N4|SAN MATEO|CA|94401?",
            "HL|3|2|22|0?",
            "TRN|1|930000000000|9800000004|PD?",
            "NM1|IL|1|DOE|JOHN||||MI|00000000001?",
            "REF|6P|0123456789?",
            "DMG|D8|19700101?",
            "DTP|291|D8|20131031?",
            "EQ|30?",
            "SE|17|0001?",
            "GE|1|1?",
            "IEA|1|000000907?",
        ]
    )


@pytest.fixture
def x12_271_subscriber_transaction() -> str:
    return "\n".join(
        [
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
        ]
    )


@pytest.fixture
def x12_271_subscriber_input(
    x12_control_header, x12_271_subscriber_transaction, x12_control_footer
) -> str:

    x12_271_header: str = x12_control_header.replace("GS01", "HB").replace(
        "GS08", "005010X279A1"
    )
    return f"{x12_271_header}{x12_271_subscriber_transaction}{x12_control_footer}"


@pytest.fixture
def x12_271_dependent_transaction() -> str:
    return "\n".join(
        [
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
        ]
    )


@pytest.fixture
def x12_271_dependent_input(
    x12_control_header, x12_271_dependent_transaction, x12_control_footer
) -> str:
    x12_271_header: str = x12_control_header.replace("GS01", "HB").replace(
        "GS08", "005010X279A1"
    )

    return f"{x12_271_header}{x12_271_dependent_transaction}{x12_control_footer}"


@pytest.fixture
def x12_837_commercial_insurance_dependent_transaction() -> str:
    return "\n".join(
        [
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
        ]
    )


@pytest.fixture
def x12_837_commercial_insurance_subscriber_transaction() -> str:
    return "\n".join(
        [
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
            "HL*2*1*22*0~",
            "SBR*P**2222-SJ******CI~",
            "NM1*IL*1*SMITH*JANE****MI*JS00111223333~",
            "NM1*PR*2*KEY INSURANCE COMPANY*****PI*999996666~",
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
            "SE*34*0021~",
        ]
    )


@pytest.fixture
def x12_837_commercial_insurance_dependent_input(
    x12_control_header,
    x12_837_commercial_insurance_dependent_transaction,
    x12_control_footer,
) -> str:
    x12_837_header: str = x12_control_header.replace("GS01", "HC").replace(
        "GS08", "005010X222A2"
    )

    return f"{x12_837_header}{x12_837_commercial_insurance_dependent_transaction}{x12_control_footer}"


@pytest.fixture
def x12_837_commercial_insurance_subscriber_input(
    x12_control_header,
    x12_837_commercial_insurance_subscriber_transaction,
    x12_control_footer,
) -> str:
    x12_837_header: str = x12_control_header.replace("GS01", "HC").replace(
        "GS08", "005010X222A2"
    )

    return f"{x12_837_header}{x12_837_commercial_insurance_subscriber_transaction}{x12_control_footer}"
