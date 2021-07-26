"""
test_x12_parser_context.py
"""
from x12.parsing import X12ParserContext


def test_init(x12_parser_context: X12ParserContext):

    assert x12_parser_context.loop_name is None
    assert x12_parser_context.loop_container == {}

    assert len(x12_parser_context.transaction_data) == 2
    assert "header" in x12_parser_context.transaction_data
    assert "footer" in x12_parser_context.transaction_data

    assert x12_parser_context.is_transaction_complete is False


def test_set_loop_context(x12_parser_context: X12ParserContext):

    x12_parser_context.set_loop_context(
        "header", x12_parser_context.transaction_data["header"]
    )
    assert x12_parser_context.loop_name == "header"
    assert x12_parser_context.loop_container == {}


def test_reset_loop_context(x12_parser_context: X12ParserContext):

    x12_parser_context.set_loop_context(
        "header", x12_parser_context.transaction_data["header"]
    )
    x12_parser_context.reset_loop_context()
    assert x12_parser_context.loop_name is None
    assert x12_parser_context.loop_container == {}


def test_reset_transaction(x12_parser_context: X12ParserContext):
    x12_parser_context.reset_transaction()
    assert x12_parser_context.transaction_data == {"header": {}, "footer": {}}
    assert x12_parser_context.is_transaction_complete is False


def test_mark_transaction_complete(x12_parser_context: X12ParserContext):
    x12_parser_context.mark_transaction_complete()
    assert x12_parser_context.is_transaction_complete is True
