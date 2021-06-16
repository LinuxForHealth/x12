"""
X12 Control segment data models
"""
from x12.models import X12BaseModel
from pydantic import Field


class IsaSegment(X12BaseModel):
    authorization_information_qualifier: str = Field(min_length=2, max_length=2)
    


class GsSegment(X12BaseModel):
    pass


class GeSegment(X12BaseModel):
    pass


class IeaSegment(X12BaseModel):
    pass
