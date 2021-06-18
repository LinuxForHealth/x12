"""
models.py

The base models for X12 parsing and validation that aren't associated with a specific X12 version.
"""
import datetime

from pydantic import BaseModel, Field
from typing import List, Optional


class X12VersionIdentifiers(BaseModel):
    """
    X12VersionIdentifiers stores the various version ids distributed in the ISA, GS, and ST control segments.
    """

    interchange_control_version: str
    functional_id_code: str = Field(min_length=2, max_length=2)
    functional_version_code: str = Field(min_length=1, max_length=12)
    transaction_set_code: str = Field(min_length=3, max_length=3)

    def __str__(self):
        """
        :return: the string representation of the Version Identifiers as a "-" delimited key
        """
        return f"{self.interchange_control_version}-{self.functional_id_code}-{self.functional_version_code}-{self.transaction_set_code}"


class X12Delimiters(BaseModel):
    """
    X12Delimiters models the common delimiters used within a X12 message's models.
    """

    element_separator: str = Field("*", min_length=1, max_length=1)
    repetition_separator: str = Field("^", min_length=1, max_length=1)
    segment_terminator: str = Field("~", min_length=1, max_length=1)
    component_separator: str = Field(":", min_length=1, max_length=1)


class X12SegmentContext(BaseModel):
    """
    Provides a working context and metadata for a X12 segment.
    """

    version: Optional[X12VersionIdentifiers] = None
    delimiters: Optional[X12Delimiters] = None
    interchange_header: Optional[List[str]] = None
    functional_group_header: Optional[List[str]] = None
    transaction_set_header: Optional[List[str]] = None
    previous_segment_name: Optional[str] = None
    previous_segment: Optional[List[str]] = None
    current_segment_name: Optional[str] = None
    current_segment: Optional[List[str]] = None
    current_loop: Optional[str] = None


class X12BaseSegmentModel(BaseModel):
    """
    X12BaseSegmentModel serves as the base class for all X12 segment models.
    """

    delimiters: X12Delimiters = X12Delimiters()
    segment_name: str = Field(min_length=2, max_length=3)

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
