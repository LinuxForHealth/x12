"""
models.py

Includes the base model used for X12 parsing and validation, in addition to models that aren't coupled to a specific
X12 version.
"""
import datetime

from pydantic import BaseModel, Field


class X12Loop(BaseModel):
    """
    Models a X12 loop, which is a logical grouping of models within a transaction set.
    """

    id: str
    description: str


class X12Delimiters(BaseModel):
    """
    X12Delimiters models the common delimiters used within a X12 message's models.
    """

    element_separator: str = Field("*", min_length=1, max_length=1)
    repetition_separator: str = Field("^", min_length=1, max_length=1)
    segment_terminator: str = Field("~", min_length=1, max_length=1)
    component_separator: str = Field(":", min_length=1, max_length=1)


class X12BaseModel(BaseModel):
    """
    X12BaseModel serves as the base class for all X12 segment models.
    """

    delimiters: X12Delimiters = X12Delimiters()
    loop_context: X12Loop
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
        model_values = [
            v for v in self.dict(exclude={"delimiters", "loop_context"}).values()
        ]
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