from api.supabase.model.point import ConsumeInfoDTO, OliveInfoDTO
from api.supabase.repo.score_repo import ScoreRepository


class PointMgr:
    def __init__(self, score_repo:ScoreRepository):
        self.score_repo = score_repo

    def consume_point(self, consume_info:ConsumeInfoDTO):
        self.score_repo.insert_used_point(consume_info)

    def consume_olive(self, olive_info:OliveInfoDTO):
        self.score_repo.update_olive_data(olive_info)

    def get_latest_consume(self, login_dto):
        return self.score_repo.check_latest_consume(login_dto.peer_id)