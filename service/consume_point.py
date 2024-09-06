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

    def get_used_point(self, login_dto):
        comsume_info: ConsumeInfoDTO = self.score_repo.get_used_point_by_id(login_dto.peer_id)
        print(f"[log] test > consume_info {comsume_info}")
        if comsume_info:
            return sum(item['used_score'] for item in comsume_info)
        return 0

    def get_score_data(self, login_dto):
        if login_dto is None:
            return None
        return self.score_repo.get_data_by_id(login_dto.peer_id)