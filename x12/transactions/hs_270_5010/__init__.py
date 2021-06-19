from pydantic import BaseModel
from .header import Header


class EligibilityInquiry(BaseModel):
    header: Header
