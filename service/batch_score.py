from api.supabase.model.nfc import EntranceInfoDTO
from api.supabase.model.quiz import ScoreInfoDTO
from api.supabase.repo.entrance_repo import EntranceRepository
from api.supabase.repo.score_repo import ScoreRepository

class BatchMgr:
    def __init__(self, enter_repo:EntranceRepository, score_repo:ScoreRepository):
        self.enter_repo = enter_repo
        self.score_repo = score_repo

    def batch_force_exit(self, entrance_info_dto:EntranceInfoDTO, score_info_dto:ScoreInfoDTO):
        pass