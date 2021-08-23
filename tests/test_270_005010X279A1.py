"""
Tests use-cases for the 270 005010X279A1 (Eligibility Inquiry) transaction
"""

from x12.io import X12ModelReader
import pytest
from pydantic import ValidationError


def test_270_subscriber(x12_270_subscriber_input, x12_270_subscriber_transaction):
    with X12ModelReader(x12_270_subscriber_input) as r:
        model_result = [m for m in r.models()]
        assert len(model_result) == 1
        assert model_result[0].x12() == x12_270_subscriber_transaction


def test_270_dependent(x12_270_dependent_input, x12_270_dependent_transaction):
    with X12ModelReader(x12_270_dependent_input) as r:
        model_result = [m for m in r.models()]
        assert len(model_result) == 1
        assert model_result[0].x12() == x12_270_dependent_transaction


def test_270_properties_subscriber_use_case(x12_270_subscriber_input):
    """
    Tests the Eligibility Inquiry property accessors with the subscriber use-case.
    The subscriber use-case does not include a dependent record.
    The input data fixture reflects conventional Eligibility usage where a transaction contains a single
    information receiver, information source, subscriber, and optionally dependent.
    """

    with X12ModelReader(x12_270_subscriber_input) as r:
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


def test_270_properties_dependent_use_case(x12_270_dependent_input):
    """
    Tests the Eligibility Inquiry property accessors with the dependent use-case.
    The dependent use-case exercises all available properties.
    The input data fixture reflects conventional Eligibility usage where a transaction contains a single
    information receiver, information source, subscriber, and optionally dependent.
    """

    with X12ModelReader(x12_270_dependent_input) as r:
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


def test_property_usage(x12_270_subscriber_input):
    """A test case used to exercise property usage"""

    with X12ModelReader(x12_270_subscriber_input) as r:
        transaction_model = [m for m in r.models()][0]

        # the property isn't cached so fetch the subscriber into a variable
        subscriber = transaction_model.subscriber
        subscriber_name = subscriber["loop_2100c"]["nm1_segment"]
        assert subscriber_name["name_last_or_organization_name"] == "DOE"
        assert subscriber_name["name_first"] == "JOHN"
        assert subscriber_name["identification_code"] == "00000000001"

        subscriber_transaction = subscriber["trn_segment"][0]
        assert subscriber_transaction["originating_company_identifier"] == "9800000004"

        info_source_name = transaction_model.information_source["loop_2100a"][
            "nm1_segment"
        ]
        assert info_source_name["name_last_or_organization_name"] == "PAYER C"
        assert info_source_name["identification_code"] == "12345"


def test_hl_segment_id_increment_validation(x12_270_subscriber_input):
    """
    Validates the hl segment id validation where ids are expected to auto-increment
    """
    # increment the id to trigger a validation error
    test_input = x12_270_subscriber_input.replace("HL*3*2*22*0~", "HL*4*1*22*0~")
    with X12ModelReader(test_input) as r:
        with pytest.raises(ValidationError):
            for _ in r.models():
                pass


def test_hl_segment_id_reference_validations(x12_270_subscriber_input):
    """
    Validates the hl segment id links throughout the transaction set
    """
    # update the parent id to an invalid value to trigger a validation error
    test_input = x12_270_subscriber_input.replace("HL*3*2*22*0~", "HL*3*10*22*0~")
    with X12ModelReader(test_input) as r:
        with pytest.raises(ValidationError):
            for _ in r.models():
                pass


def test_validate_subscriber_hierarchy_child_code(x12_270_subscriber_input):
    # update the hierarchy child code to "1" to trigger a validation error
    # update the parent id to an invalid value to trigger a validation error
    test_input = x12_270_subscriber_input.replace("HL*3*2*22*0~", "HL*3*2*22*1~")
    with X12ModelReader(test_input) as r:
        with pytest.raises(ValidationError):
            for _ in r.models():
                pass


def test_validate_subscriber_name(x12_270_subscriber_input):
    # remove the first name from the subscriber segment to trigger a validation error
    test_input = x12_270_subscriber_input.replace(
        "NM1*IL*1*DOE*JOHN****MI*00000000001~", "NM1*IL*1*DOE*****MI*00000000001~"
    )
    with X12ModelReader(test_input) as r:
        with pytest.raises(ValidationError):
            for _ in r.models():
                pass


def test_validate_information_source_id_codes(x12_270_subscriber_input):
    # remote the id code value from the information source to trigger a validation error
    test_input = x12_270_subscriber_input.replace(
        "NM1*PR*2*PAYER C*****PI*12345~", "NM1*PR*2*PAYER C*****PI~"
    )
    with X12ModelReader(test_input) as r:
        with pytest.raises(ValidationError):
            for _ in r.models():
                pass


def test_validate_ref_segment_usage(x12_270_subscriber_input):
    # update the input to include duplicate REF segments
    test_input = x12_270_subscriber_input.replace(
        "REF*4A*000111222~", "REF*4A*000111222~REF*4A*444222999~"
    )
    with X12ModelReader(test_input) as r:
        with pytest.raises(ValidationError):
            for _ in r.models():
                pass


def test_validate_n4_state_codes(x12_270_subscriber_input):
    # update the input to include duplicate REF segments
    test_input = x12_270_subscriber_input.replace(
        "N4*SAN MATEO*CA*94401~", "N4*SAN MATEO*CA*94401****US-AS~"
    )
    with X12ModelReader(test_input) as r:
        with pytest.raises(ValidationError):
            for _ in r.models():
                pass


def test_validate_prv_reference_codes(x12_270_subscriber_input):
    # update the input to include duplicate REF segments
    test_input = x12_270_subscriber_input.replace(
        "PRV*PC*HPI*3435612668~", "PRV*PC*HPI~"
    )
    with X12ModelReader(test_input) as r:
        with pytest.raises(ValidationError):
            for _ in r.models():
                pass


def test_validate_date_fields(x12_270_subscriber_input):
    # update the input to remove the date_time_format_qualifier field
    test_input = x12_270_subscriber_input.replace("DMG*D8*19700101~", "DMG**19700101~")
    with X12ModelReader(test_input) as r:
        with pytest.raises(ValidationError):
            for _ in r.models():
                pass


def test_validate_eq_segment_coding(x12_270_subscriber_input):
    # update the input to remove the date_time_format_qualifier field
    test_input = x12_270_subscriber_input.replace("EQ*30~", "EQ~")
    with X12ModelReader(test_input) as r:
        with pytest.raises(ValidationError):
            for _ in r.models():
                pass
