"""
encoding.py

Custom JSON Encoder used to support data types not included in the JSON Specification.
"""
from typing import Any
from json import JSONEncoder
import datetime
import uuid
import base64
import decimal


class X12JsonEncoder(JSONEncoder):
    """
    Provides additional encoding support for the following types:
    - UUID fields
    - date, datetime, and time fields
    - byte fields
    - Decimal fields
    """

    def default(self, o: Any) -> Any:
        """
        Overridden to customize the encoding process.
        :param o: The current object to encode
        """
        if isinstance(o, (datetime.date, datetime.datetime, datetime.time)):
            return o.isoformat()
        elif isinstance(o, uuid.UUID):
            return str(o)
        elif isinstance(o, bytes):
            return base64.b64encode(o).decode()
        elif isinstance(o, decimal.Decimal):
            return float(o)
        else:
            return super().default(o)
