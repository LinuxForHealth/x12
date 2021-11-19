"""
cli.py

The LinuxForHealth X12 Command Line Interface.

Usage:
    pipenv run cli --help

"""

import argparse
import json
from .encoding import X12JsonEncoder
from .io import X12SegmentReader, X12ModelReader
from typing import List


CLI_DESCRIPTION = """
The LinuxForHealth X12 CLI parses and validates X12 messages.
Messages are returned in JSON format in either a segment or transactional format.
"""


def _create_arg_parser():
    """
    Creates the Argument Parser for the CLI utility.
    :return: ArgumentParser
    """

    parser = argparse.ArgumentParser(
        prog="LinuxForHealth X12",
        description=CLI_DESCRIPTION,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "-s", "--segment", help="Returns X12 segments", action="store_true"
    )
    mode_group.add_argument(
        "-m", "--model", help="Returns X12 models", action="store_true"
    )

    parser.add_argument(
        "-x",
        "--exclude",
        help="Exclude fields set to None in model output",
        action="store_true",
    )
    parser.add_argument(
        "-p", "--pretty", help="Pretty print output", action="store_true"
    )

    parser.add_argument("file", help="The path to a ASC X12 file")

    return parser.parse_args()


def _parse_segments(file_path: str) -> List:
    """
    Parses X12 segments from an input file.

    :param file_path: The path to the X12 file.
    :return: List of X12 segments
    """

    with X12SegmentReader(file_path) as r:
        segments = []

        for segment_name, segment in r.segments():
            segment_data = {
                f"{segment_name}{str(i).zfill(2)}": v for i, v in enumerate(segment)
            }
            segments.append(segment_data)
        return segments


def _parse_models(file_path: str, exclude_none: bool = False) -> List:
    """
    Parses a X12 segment model from a X12 input file.

    :param file_path: The path to the X12 file.
    :param exclude_none: Excludes fields set to None from the model output.
    :return: List of X12 models
    """

    with X12ModelReader(file_path) as r:
        models = []
        for m in r.models():
            model_data = m.dict(exclude_unset=exclude_none, exclude_none=exclude_none)
            models.append(model_data)
        return models


def main():
    """
    CLI module entrypoint
    """
    args = _create_arg_parser()

    x12_data = (
        _parse_segments(args.file)
        if args.segment
        else _parse_models(args.file, args.exclude)
    )

    json_opts = {"cls": X12JsonEncoder}

    if args.pretty:
        json_opts["indent"] = 4

    x12_json = json.dumps(x12_data, **json_opts)
    print(x12_json)
