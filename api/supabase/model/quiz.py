from typing import Optional

from pydantic import BaseModel
from datetime import datetime

class ScoreInfoDTO(BaseModel):
    id: int
    created_at: Optional[datetime] = None
    quiz_dvcd: int
    company_dvcd: int
    score: float

    class Config:
        from_attributes = True

class RankDTO(BaseModel):
    id: int
    total_score: float
    rank: int
    name: Optional[str]  # 값이 없을 수 있는 문자열
    company: Optional[str]  # 값이 없을 수 있는 문자열

    class Config:
        from_attributes = True