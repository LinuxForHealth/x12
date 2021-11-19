import pytest
from typing import Callable, Dict
from linuxforhealth.x12.parsing import X12ParserContext, match


@pytest.fixture
def segment_data(x12_delimiters) -> Dict:
    return {
        "delimiters": x12_delimiters.dict(),
        "segment_name": "ST",
        "transaction_set_identifier_code": "270",
        "transaction_set_control_number": "0001",
        "implementation_convention_reference": "005010X279A1",
    }


@pytest.fixture
def parser_function() -> Callable:
    def func(x12_parser_context: X12ParserContext, segment_data: Dict):
        x12_parser_context.parsed_loops.append("test_loop")

    return func


def test_match_no_conditions(parser_function, segment_data, x12_parser_context):
    """
    Tests the match decorator when no conditions are specified.
    """
    wrapped_func = match("ST")(parser_function)
    wrapped_func(segment_data, x12_parser_context)
    assert x12_parser_context.loop_name == "test_loop"


def test_single_match_condition(parser_function, segment_data, x12_parser_context):
    """
    Tests the match decorator when a single condition is specified.
    """
    wrapped_func = match("ST", conditions={"transaction_set_identifier_code": "270"})(
        parser_function
    )
    wrapped_func(segment_data, x12_parser_context)
    assert x12_parser_context.loop_name == "test_loop"


def test_multiple_match_condition(parser_function, segment_data, x12_parser_context):
    """
    Tests the match decorator when multiple conditions are specified.
    """
    wrapped_func = match(
        "ST",
        conditions={
            "transaction_set_identifier_code": "270",
            "transaction_set_control_number": "0001",
        },
    )(parser_function)
    wrapped_func(segment_data, x12_parser_context)
    assert x12_parser_context.loop_name == "test_loop"


def test_list_match_condition(parser_function, segment_data, x12_parser_context):
    """
    Tests the match decorator when a list/"one of" condition is specified.
    """
    wrapped_func = match(
        "ST", conditions={"transaction_set_identifier_code": ["270", "276"]}
    )(parser_function)
    wrapped_func(segment_data, x12_parser_context)
    assert x12_parser_context.loop_name == "test_loop"


def test_match_conditions_unmatched(parser_function, segment_data, x12_parser_context):
    """
    Tests the match decorator when conditions are specified but they do not match the data_segment.
    """
    wrapped_func = match("ST", conditions={"transaction_set_identifier_code": "911"})(
        parser_function
    )
    wrapped_func(segment_data, x12_parser_context)
    assert x12_parser_context.loop_name is None
