from x12.io import X12SegmentReader


def test_x12_reader_context(simple_270_one_line):
    """
    Tests the X12 reader context object during x12 segment iteration
    """

    with X12SegmentReader(simple_270_one_line) as r:
        # validates delimiters
        assert r.context.delimiters.component_separator == ":"
        assert r.context.delimiters.element_separator == "*"
        assert r.context.delimiters.repetition_separator == "^"
        assert r.context.delimiters.segment_terminator == "~"

        total_segment_count = 0
        parsed_transaction_set = False

        for segment_name, segment, context in r.segments():
            # validate current
            assert r.context.current_segment == segment
            assert r.context.current_segment_name == segment_name

            total_segment_count += 1

            if segment_name == "ST":
                is_version_tested = True
                assert str(r.context.version) == "HS_270_00501"
        else:
            # confirm that we iterated
            assert is_version_tested is True
            assert 21 == total_segment_count
            assert 17 == r.context.segment_count["0001"]


def test_reader_context_helpers(simple_270_one_line):
    """
    Tests the reader "context" helpers used to determine if a segment is a control or transaction metadata segment.
    """
    control_segments = ("ISA", "GS", "GE", "IEA")

    with X12SegmentReader(simple_270_one_line) as r:
        for segment_name, segment, context in r.segments():
            assert (
                bool(segment_name in control_segments) is r.is_control_segment()
            ), f"{segment_name} is not a control segment"

            assert bool(segment_name == "ISA") is r.is_interchange_header()
            assert bool(segment_name == "IEA") is r.is_interchange_footer()
            assert bool(segment_name == "GS") is r.is_functional_group_header()
            assert bool(segment_name == "GE") is r.is_functional_group_footer()
            assert bool(segment_name == "ST") is r.is_transaction_header()
            assert bool(segment_name == "SE") is r.is_transaction_footer()
