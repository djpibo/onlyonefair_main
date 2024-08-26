from typing import Optional

from pydantic import BaseModel
from datetime import datetime

class PeerInfoDTO(BaseModel):
    id: int
    created_at: Optional[datetime] = None
    company: str
    name: str
    nfc_id: str

    class Config:
        from_attributes = True