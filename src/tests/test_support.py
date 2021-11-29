"""
test_support.py

Tests support functions.
"""
import pytest
import datetime
from linuxforhealth.x12.support import (
    is_x12_data,
    is_x12_file,
    parse_x12_date,
    parse_interchange_date,
    count_segments,
    parse_x12_major_version,
)
from linuxforhealth.x12.io import X12ModelReader


@pytest.mark.parametrize(
    "test_input, is_fixture, expected",
    [
        ("simple_270_with_new_lines", True, True),
        ("simple_270_one_line", True, True),
        ("foo", False, False),
        ("", False, False),
        (None, False, False),
    ],
)
def test_is_x12_data(request, test_input: str, is_fixture: bool, expected: bool):
    """
    Tests is_x12_data with fixtures and literal values.
    :param request: The pytest request fixture. Used to lookup fixture values by name.
    :param test_input: The fixture name or the literal value.
    :param is_fixture: Indicates if test_input is a fixture name.
    :param expected: The expected test value
    """

    input_value = request.getfixturevalue(test_input) if is_fixture else test_input
    assert is_x12_data(input_value) is expected


@pytest.mark.parametrize(
    "test_input", ["simple_270_with_new_lines", "simple_270_one_line"]
)
def test_is_x12_file_true(request, tmpdir, test_input: str):
    """
    Tests is_x12_file where the expected result is True.
    :param request: The pytest request fixture. Used to lookup fixture values by name.
    :param tmpdir: The pytest tmpdir fixture. Used to create tmp directory and files.
    :param test_input: The fixture name.
    """

    input_value = request.getfixturevalue(test_input)
    f = tmpdir.mkdir("x12-support").join("test.x12")
    f.write(input_value)

    assert is_x12_file(f)


def test_is_x12_file_false():
    assert is_x12_file("/home/not-a-real/file.txt") is False
    assert is_x12_file("") is False
    assert is_x12_file(None) is False


def test_parser_interchange_date():
    assert parse_interchange_date("131031") == datetime.date(2013, 10, 31)


def test_parse_x12_date():
    assert parse_x12_date("20120501") == datetime.date(2012, 5, 1)
    assert parse_x12_date("201205011010") == datetime.datetime(2012, 5, 1, 10, 10)
    assert parse_x12_date("") is None
    assert parse_x12_date(None) is None


def test_count_segments(simple_270_with_new_lines):
    with X12ModelReader(simple_270_with_new_lines) as r:
        model = [m for m in r.models()][0]
        model_data = model.dict()
        segment_count: int = count_segments(model_data)
        assert segment_count == 17


def test_parse_x12_major_version():
    assert parse_x12_major_version("005010X279A1") == "5010"
    assert parse_x12_major_version("00501") == ""
    assert parse_x12_major_version(None) == ""
