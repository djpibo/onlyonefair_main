from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class ScoreInfoDTO(BaseModel):
    id: int
    created_at: Optional[datetime] = None
    quiz_dvcd: int
    company_dvcd: int
    score: float = 0

    class Config:
        from_attributes = True

class RankDTO(BaseModel):
    id: int
    total_score: Optional[float]
    rank: Optional[int]
    name: Optional[str]  # 값이 없을 수 있는 문자열
    company: Optional[str]  # 값이 없을 수 있는 문자열
    room_score: Optional[float]
    quiz_score: Optional[float]
    photo_score: Optional[float]
    survey_score: Optional[float]

    class Config:
        from_attributes = True