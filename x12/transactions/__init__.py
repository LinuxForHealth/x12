"""
transactions package
"""
import functools
import importlib

from pydantic import BaseModel

# maps python packages used to support a x12 transaction to the x12 transaction class
_transaction_map = {
    "x12_270_005010X279A1": "EligibilityInquiry",
    "x12_271_005010X279A1": "EligibilityInformation",
}


@functools.lru_cache(typed=True)
def get_transaction_model(
    transaction_code: str, implementation_reference: str
) -> BaseModel:
    transaction_package = f"x12_{transaction_code}_{implementation_reference}"
    model_name = _transaction_map[transaction_package]

    transaction_module = importlib.import_module(
        f"x12.transactions.{transaction_package}"
    )
    transaction_model = getattr(transaction_module, model_name)

    return transaction_model
