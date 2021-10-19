"""
Tests use-cases for the 271 005010X279A1 (Eligibility Benefit Response) transaction
"""
from x12.io import X12ModelReader
import pytest
from tests.support import assert_eq_model, resources_directory
import os


@pytest.fixture
def resource_path() -> str:
    return os.path.join(resources_directory, "271_005010X279A1")


@pytest.mark.parametrize(
    "file_name",
    ["dependent.271", "subscriber.271"],
)
def test_271_model(resource_path, file_name: str):
    x12_file_path = os.path.join(resource_path, file_name)
    assert os.path.exists(x12_file_path)
    assert_eq_model(x12_file_path)


def test_271_properties_subscriber_use_case(resource_path: str):
    """
    Tests the Eligibility Benefit property accessors with the subscriber use-case.
    The subscriber use-case does not include a dependent record.
    The input data fixture reflects conventional Eligibility usage where a transaction contains a single
    information receiver, information source, subscriber, and optionally dependent.

    :param resource_path: The path to the directory containing x12 test files
    """
    x12_file = os.path.join(resource_path, "subscriber.271")
    assert os.path.exists(x12_file)

    with X12ModelReader(x12_file) as r:
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


def test_271_properties_dependent_use_case(resource_path: str):
    """
    Tests the Eligibility Benefit property accessors with the dependent use-case.
    The input data fixture reflects conventional Eligibility usage where a transaction contains a single
    information receiver, information source, subscriber, and optionally dependent.

    :param resource_path: The path to the directory containing x12 test files
    """
    x12_file = os.path.join(resource_path, "dependent.271")
    assert os.path.exists(x12_file)

    with X12ModelReader(x12_file) as r:
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
