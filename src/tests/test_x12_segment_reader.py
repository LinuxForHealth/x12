"""
Tests LinuxForHealth X12SegmentReader
"""
import pytest

import linuxforhealth.x12.io
from linuxforhealth.x12.io import X12SegmentReader


@pytest.mark.parametrize(
    "test_input", ["simple_270_with_new_lines", "simple_270_one_line"]
)
def test_init(request, test_input: str):
    """
    Tests X12SegmentReader initialization

    :param request: The pytest request fixture. Used to lookup fixture values by name.
    :param test_input: The fixture name.
    """

    input_value = request.getfixturevalue(test_input)
    x12_reader = X12SegmentReader(input_value)
    assert x12_reader._x12_input
    assert x12_reader._buffer_size is None
    assert x12_reader._x12_stream is None
    assert x12_reader.delimiters is None


@pytest.mark.parametrize(
    "test_input", ["simple_270_with_new_lines", "simple_270_one_line"]
)
def test_segments_with_string_data(request, test_input: str):
    """
    Test X12SegmentReader models with a x12 data/message input.

    :param request: The pytest request fixture. Used to lookup fixture values by name.
    :param test_input: The fixture name.
    """

    input_value = request.getfixturevalue(test_input)

    with X12SegmentReader(input_value) as r:
        segment_count = 0

        assert r.delimiters.component_separator == ":"
        assert r.delimiters.element_separator == "*"
        assert r.delimiters.repetition_separator == "^"
        assert r.delimiters.segment_terminator == "~"

        for _ in r.segments():
            segment_count += 1

        assert 21 == segment_count

    assert r._x12_stream.closed
    assert r.delimiters is None
    assert r._x12_input is None


@pytest.mark.parametrize(
    "test_input", ["simple_270_with_new_lines", "simple_270_one_line"]
)
def test_segments_with_file_path(request, tmpdir, test_input: str):
    """
    Test X12SegmentReader models with a x12 file path input.

    :param request: The pytest request fixture. Used to lookup fixture values by name.
    :param tmpdir: Pytest fixture used to create temporary files and directories
    :param test_input: The fixture name.
    """

    input_value = request.getfixturevalue(test_input)
    f = tmpdir.mkdir("x12-support").join("test.x12")
    f.write(input_value)

    with X12SegmentReader(f) as r:
        segment_count = 0
        version_key = None

        assert r.delimiters.component_separator == ":"
        assert r.delimiters.element_separator == "*"
        assert r.delimiters.repetition_separator == "^"
        assert r.delimiters.segment_terminator == "~"

        for _ in r.segments():
            segment_count += 1

        assert 21 == segment_count

    assert r._x12_stream.closed
    assert r.delimiters is None
    assert r._x12_input is None


def test_invalid_x12_data(simple_270_one_line):
    """
    Tests an invalid x12 message input.
    :param simple_270_one_line: X12 Fixture
    """

    invalid_x12 = simple_270_one_line.replace("ISA", "FOO")

    with pytest.raises(ValueError):
        with X12SegmentReader(invalid_x12) as r:
            for _ in r.segments():
                assert False, "Expecting ValueError Exception"


def test_invalid_x12_file(tmpdir, simple_270_one_line):
    """
    Tests an invalid x12 file path input.
    :param tmpdir: Pytest fixture used to create temp files and directories.
    :param simple_270_one_line: X12 Fixture
    """

    invalid_x12 = simple_270_one_line.replace("ISA", "FOO")
    f = tmpdir.mkdir("x12-support").join("test.x12")
    f.write(invalid_x12)

    with pytest.raises(ValueError):
        with X12SegmentReader(f.strpath) as r:
            for _ in r.segments():
                assert False, "Expecting ValueError Exception"


def test_large_x12_message(monkeypatch, large_x12_message, config):
    """
    Tests a large x12 message to validate buffering.
    :param monkeypatch: Pytest fixture for monkeypatching/mocking code.
    :param large_x12_message: Large X12 message fixture
    :param config: X12 configuration fixture
    """

    def mock_get_config():
        return config

    with monkeypatch.context() as m:
        m.setattr(linuxforhealth.x12.io, "get_config", mock_get_config)

        segment_counter = 0
        with X12SegmentReader(large_x12_message) as r:
            for _ in r.segments():
                segment_counter += 1

        assert r._x12_stream.closed
        assert segment_counter == 174
