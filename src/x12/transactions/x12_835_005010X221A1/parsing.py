"""
parsing.py

Parses X12 835 005010X221A1 segments into a transactional domain model.

The parsing module includes a specific parser for the 835 transaction and loop parsing functions to create new loops
as segments are streamed to the transactional data model.

Loop parsing functions are implemented as set_[description]_loop(context: X12ParserContext, segment_data: Dict).
"""
