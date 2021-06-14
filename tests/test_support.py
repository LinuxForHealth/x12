"""
test_support.py

Tests support functions.
"""
from x12.support import is_x12_data, is_x12_file, os
import pytest


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
