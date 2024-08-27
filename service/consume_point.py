from api.supabase.model.point import ConsumeInfoDTO
from api.supabase.model.quiz import ScoreInfoDTO
from api.supabase.repo.score_repo import ScoreRepository


class PointMgr:
    def __init__(self, score_repo:ScoreRepository):
        self.score_repo = score_repo

    def consume_point(self, consume_info:ConsumeInfoDTO):
        self.score_repo.insert_used_point(consume_info)