"""
models.py

The base models for X12 parsing and validation that aren't associated with a specific X12 version.
"""
import abc
import datetime
from typing import List
from enum import Enum
from pydantic import BaseModel, Field


class X12Delimiters(BaseModel):
    """
    X12Delimiters models the common delimiters used within a X12 message's models.
    """

    element_separator: str = Field("*", min_length=1, max_length=1)
    repetition_separator: str = Field("^", min_length=1, max_length=1)
    segment_terminator: str = Field("~", min_length=1, max_length=1)
    component_separator: str = Field(":", min_length=1, max_length=1)


class X12SegmentName(str, Enum):
    """
    Supported X12 Segment Names
    """

    BHT = "BHT"
    GE = "GE"
    GS = "GS"
    HL = "HL"
    IEA = "IEA"
    ISA = "ISA"
    NM1 = "NM1"
    SE = "SE"
    ST = "ST"


class X12Segment(abc.ABC, BaseModel):
    """
    X12BaseSegment serves as the abstract base class for all X12 segment models.
    """

    delimiters: X12Delimiters = X12Delimiters()
    segment_name: X12SegmentName

    class Config:
        """
        Default configuration for X12 Models
        """

        use_enum_values = True

    def x12(self) -> str:
        """
        :return: the X12 representation of the model instance
        """
        model_values = [v for v in self.dict(exclude={"delimiters"}).values()]
        x12_values = []
        for v in model_values:
            if isinstance(v, str):
                x12_values.append(v)
            elif isinstance(v, list):
                repeating_values = self.delimiters.repetition_separator.join(v)
                x12_values.append(repeating_values)
            elif isinstance(v, datetime.date):
                x12_values.append(v.isoformat().replace("-", ""))
            elif isinstance(v, datetime.time):
                x12_values.append(v.isoformat().replace(":", ""))
            elif v is None:
                x12_values.append("")
            else:
                x12_values.append(str(v))

        x12_str = self.delimiters.element_separator.join(x12_values).rstrip(
            self.delimiters.element_separator
        )
        return x12_str + self.delimiters.segment_terminator


class X12SegmentGroup(abc.ABC, BaseModel):
    """
    Abstract base class for a model, typically a loop or transaction, which groups x12 segments.
    """

    def x12(self, use_new_lines=True) -> str:
        """
        :return: Generates a X12 representation of the loop using its segments.
        """
        x12_segments: List[str] = []
        fields = [f for f in self.__fields__.values() if hasattr(f.type_, "x12")]

        for f in fields:
            field_instance = getattr(self, f.name)
            x12_segments.append(field_instance.x12())

        join_char: str = "\n" if use_new_lines else ""
        return join_char.join(x12_segments)
