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
                assert str(r.context.version) == "00501_HS_005010X279A1_270"
        else:
            # confirm that we iterated
            assert 21 == total_segment_count
            assert 17 == r.context.segment_count["0001"]
