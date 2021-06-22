"""
loops.py

Models the loops, or logical segment groupings, for the Eligibility 270 5010 transaction set
"""
from pydantic import BaseModel

from x12.segments import HlSegment


class Loop2000A(BaseModel):
    hl_segment: HlSegment
