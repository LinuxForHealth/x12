"""
test_encoding.py

Tests the X12 Custom JSON Encoder
"""
from x12.encoding import X12JsonEncoder
from decimal import Decimal
import uuid
import json
import datetime


def test_encoding():
    input_data = {
        "product": "thing-a-magigs",
        "quantity": Decimal("4.89"),
        "order_date": datetime.date(2021, 7, 15),
        "id": uuid.UUID("11ae9671-f227-48e9-ad4c-565120b7fa8f"),
    }

    result: str = json.dumps(input_data, cls=X12JsonEncoder)
    # compare with "in" since order isn't guaranteed
    assert '"product": "thing-a-magigs"' in result
    assert '"quantity": 4.89' in result
    assert '"order_date": "2021-07-15"' in result
    assert '"id": "11ae9671-f227-48e9-ad4c-565120b7fa8f"' in result
