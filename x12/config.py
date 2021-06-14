"""
config.py
"""
from pydantic import BaseSettings, Field
import os
from os.path import dirname, abspath
from functools import lru_cache


class X12Config(BaseSettings):
    """
    X12 Parsing and Validation Configurations
    """

    isa_element_separator: int = 3
    isa_repetition_separator: int = 82
    isa_segment_length: int = 106
    isa_segment_terminator: int = 105

    x12_character_set: str = Field(regex="^(BASIC|EXTENDED)$")
    x12_reader_buffer_size: int = 1024000

    class Config:
        case_sensitive = False
        env_file = os.path.join(dirname(dirname(abspath(__file__))), ".env")


@lru_cache
def get_config():
    """Returns the X12Config"""
    return X12Config()
