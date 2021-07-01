"""
config.py

LinuxForHealth X12 Configuration Settings and specification/format "constants"
"""
import os
from enum import IntEnum
from functools import lru_cache
from os.path import abspath, dirname

from pydantic import BaseSettings, Field


class IsaDelimiters(IntEnum):
    """
    The indices used to parse the delimiters conveyed in the ISA segment
    """

    COMPONENT_SEPARATOR: int = 104
    ELEMENT_SEPARATOR: int = 3
    REPETITION_SEPARATOR: int = 82
    SEGMENT_LENGTH: int = 106
    SEGMENT_TERMINATOR: int = 105


class TransactionSetVersionIds(IntEnum):
    """
    The indices used to parse transaction set version identifiers
    """

    TRANSACTION_SET_CODE = 1
    IMPLEMENTATION_VERSION = 3


class X12VersionFields(IntEnum):
    """
    Positional field indices for X12 version fields
    """

    ISA_CONTROL_VERSION: int = 12
    GS_FUNCTIONAL_CODE: int = 1
    GS_FUNCTIONAL_VERSION: int = 8
    ST_TRANSACTION_CODE: int = 1
    ST_TRANSACTION_CONTROL: int = 2


class X12Config(BaseSettings):
    """
    X12 Parsing and Validation Configurations
    """

    x12_character_set: str = Field(regex="^(BASIC|EXTENDED)$")
    x12_reader_buffer_size: int = 1024000

    class Config:
        case_sensitive = False
        env_file = os.path.join(dirname(dirname(abspath(__file__))), ".env")


@lru_cache
def get_config():
    """Returns the X12Config"""
    return X12Config()
