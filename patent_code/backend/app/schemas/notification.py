from pydantic import BaseModel
from typing import Any, Dict


class NotificationRead(BaseModel):
    id: int
    type: str
    payload: Dict[str, Any]
    delivered: bool

    class Config:
        orm_mode = True
