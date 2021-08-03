"""
Tests use-cases for the 005010X279A1 (Eligibility Inquiry and Response) transactions
"""

from x12.io import X12ModelReader


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
