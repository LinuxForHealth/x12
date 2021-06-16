"""
control_segments.py

Data models for X12 Control Segments that are not coupled to a specific X12 version.
"""
from x12.models import X12BaseModel
from x12.v5010.control_codes import *
from pydantic import Field, conint
import datetime
from typing import Literal, Union


class IsaSegment(X12BaseModel):
    """
    The interchange control header for X12 transactions
    """
    authorization_information_qualifier: AuthorizationInformationQualifier = (
        AuthorizationInformationQualifier.NO_AUTHORIZATION_PRESENT
    )
    authorization_information: str = Field("", max_length=10)
    security_information_qualifier: str = Field("", max_length=2)
    security_information: str = Field("", max_length=10)
    sender_id_qualifier: InterchangeIdQualifier = InterchangeIdQualifier.MUTUALLY_DEFINED
    sender_id: str = Field("", max_length=15)
    receiver_id_qualifier: InterchangeIdQualifier = InterchangeIdQualifier.MUTUALLY_DEFINED
    receiver_id: str = Field("", max_length=15)
    interchange_date: Union[datetime.date, str]
    interchange_time: Union[datetime.time, str]
    repetition_separator: str = Field("^", min_length=1, max_length=1)
    interchange_control_version: Literal["00501"] = "00501"
    interchange_control_number: conint(gt=0, lt=1_000_000_000)
    acknowledgment_requested: AcknowledgmentRequested = AcknowledgmentRequested.NO_ACKNOWLEDGMENT_REQUESTED
    interchange_usage: InterchangeUsage = InterchangeUsage.TEST
    component_element_separator: str = Field(":", min_length=1, max_length=1)

    def x12(self) -> str:
        """
        Overriden to provide field padding and format time fields
        :return:the X12 string
        """
        self.authorization_information = self.authorization_information.ljust(10)
        self.security_information_qualifier = self.security_information_qualifier.ljust(2)
        self.security_information = self.security_information.ljust(10)
        self.sender_id = self.sender_id.ljust(15)
        self.receiver_id = self.receiver_id.ljust(15)

        self.interchange_date = self.interchange_date.isoformat().replace("-", "")[2:]
        self.interchange_time = self.interchange_time.isoformat().replace(":", "")[0:4]
        return super().x12()


class IeaSegment(X12BaseModel):
    pass
