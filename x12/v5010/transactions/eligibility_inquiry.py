"""
eligibility_inquiry.py

Domain models for the Eligibility Inquiry "request" (270) transaction set.
"""
from pydantic import BaseModel


class EligibilityInquiry(BaseModel):
    pass


class EligibilityInformation(BaseModel):
    pass
