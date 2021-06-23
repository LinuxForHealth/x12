"""
loops.py

Models the loops, or logical segment groupings, for the Eligibility 270 5010 transaction set
"""
from pydantic import BaseModel


class Header(BaseModel):
    pass


class Loop2000A(BaseModel):
    pass
