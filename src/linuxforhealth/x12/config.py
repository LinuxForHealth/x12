"""
config.py

LinuxForHealth X12 Configuration Settings and specification/format "constants"
"""
from enum import IntEnum
from functools import lru_cache
from pydantic import BaseSettings, Field


class IsaDelimiters(IntEnum):
    """
    The indices used to parse the delimiters conveyed in the ISA segment
    """

    COMPONENT_SEPARATOR = 104
    ELEMENT_SEPARATOR = 3
    REPETITION_SEPARATOR = 82
    SEGMENT_LENGTH = 106
    SEGMENT_TERMINATOR = 105


class TransactionSetVersionIds(IntEnum):
    """
    The indices used to parse transaction set version identifiers.
    Transaction set version identifiers are distributed across the ST (transaction set header) and GS (functional group
    header) segments.
    """

    # ST01
    TRANSACTION_SET_CODE = 1
    # GS08
    IMPLEMENTATION_VERSION = 8
    # ST03
    FALLBACK_IMPLEMENTATION_VERSION = 3


class X12VersionFields(IntEnum):
    """
    Positional field indices for X12 version fields
    """

    ISA_CONTROL_VERSION = 12
    GS_FUNCTIONAL_CODE = 1
    GS_FUNCTIONAL_VERSION = 8
    ST_TRANSACTION_CODE = 1
    ST_TRANSACTION_CONTROL = 2


class X12Config(BaseSettings):
    """
    X12 Parsing and Validation Configurations
    """

    x12_character_set: str = Field(regex="^(BASIC|EXTENDED)$", default="BASIC")
    x12_reader_buffer_size: int = 1024000

    class Config:
        case_sensitive = False


@lru_cache
def get_config() -> "X12Config":
    """Returns the X12Config"""
    return X12Config()
