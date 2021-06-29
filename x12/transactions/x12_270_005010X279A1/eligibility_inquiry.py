from pydantic import BaseModel
from .loops import Header, Footer, Loop2000A
from typing import List

"""
"""


class EligibilityInquiry(BaseModel):
    """ """

    header: Header
    loop_2000A: List[Loop2000A]
    footer: Footer
