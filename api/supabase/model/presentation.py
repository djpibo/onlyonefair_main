from typing import Optional

from pydantic import BaseModel

class ScreenDTO(BaseModel):
    peer_name: Optional[str]
    enter_dvcd_kor: Optional[str]
    acc_score: Optional[float]
    current_score: Optional[float]

    class Config:
        from_attributes = True