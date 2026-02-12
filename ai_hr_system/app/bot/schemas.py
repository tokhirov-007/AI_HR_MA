from enum import Enum
from pydantic import BaseModel
from typing import Optional

class HRAction(str, Enum):
    INVITE = "invite"
    REJECT = "reject"
    REVIEW = "review"

class ActionCallbackData(BaseModel):
    action: HRAction
    session_id: str
