"""
conftest.py

Pytest Global Fixtures
"""
import pytest

from linuxforhealth.x12.config import X12Config
from linuxforhealth.x12.models import X12Delimiters
from linuxforhealth.x12.parsing import X12ParserContext


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
    # will create 10 transaction sets
    for i in range(1, 11, 1):
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
