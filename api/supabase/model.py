from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class ScreenDTO(BaseModel):
    peer_name: Optional[str]
    peer_company: Optional[str]
    comment: Optional[str]
    acc_score: Optional[float]
    used_score: Optional[float] = 0
    current_score: Optional[float] = 0
    enter_dvcd_kor: Optional[str] = None
    require_time: Optional[int] = 0

class LoginDTO(BaseModel):
    peer_id: int
    argv_company_dvcd: int
    peer_name: Optional[str] = None
    peer_company: Optional[str] = None
    enter_dvcd: Optional[int] = None

    class Config:
        from_attributes = True

class EntranceInfoDTO(BaseModel):
    id: int
    created_at: Optional[datetime] = None
    enter_dvcd: int
    company_dvcd: int
    seqno: int
    exit_yn: bool

    class Config:
        from_attributes = True

class CountInfoDTO(BaseModel):
    id: int
    created_at: Optional[datetime] = None
    seqno: Optional[int] = None

    class Config:
        from_attributes = True

class ConsumeInfoDTO(BaseModel):
    id: int
    created_at: Optional[datetime] = None
    seqno: Optional[int] = None
    consume_dvcd: int
    used_score: float
    cancel_yn: Optional[bool] = False

    class Config:
        from_attributes = True

class ScoreInfoDTO(BaseModel):
    id: int
    created_at: Optional[datetime] = None
    quiz_dvcd: int
    company_dvcd: int
    score: float

    class Config:
        from_attributes = True


class PeerInfoDTO(BaseModel):
    id: int
    created_at: Optional[datetime] = None
    company: str
    name: str
    nfc_id: str
    grade: Optional[int] = 0

    class Config:
        from_attributes = True
