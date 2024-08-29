import time

from api.google.sheet_client import GoogleSheetsClient
from api.supabase.model.nfc import EntranceInfoDTO
from api.supabase.model.point import ConsumeInfoDTO, OliveInfoDTO
from api.supabase.model.quiz import RankDTO, ScoreInfoDTO
from api.supabase.repo.common_repo import CommonRepository
from api.supabase.repo.entrance_repo import EntranceRepository
from api.supabase.repo.score_repo import ScoreRepository
from common.config import *
from common.constants import *
from common.util import CommonUtil, MapperUtil


class EnterMgr:
    def __init__(self
                 , entrance_repo: EntranceRepository
                 , common_repo: CommonRepository
                 , score_repo: ScoreRepository):
        self.entrance_repo = entrance_repo
        self.common_repo = common_repo
        self.score_repo = score_repo

    def get_unchecked_exit(self, login_dto):
        return self.entrance_repo.check_exit_yn_the_others(login_dto.peer_id, login_dto.argv_company_dvcd)

    def check_exit_before(self, login_dto):
        return self.entrance_repo.fetch_latest_exit(login_dto.peer_id, login_dto.argv_company_dvcd)

    def set_to_enter(self, login_dto):
        dto = EntranceInfoDTO(
            id= login_dto.peer_id,
            enter_dvcd= ENTER_DVCD_ENTRANCE,
            company_dvcd= login_dto.argv_company_dvcd,
            seqno= 1,
            exit_yn= False
        )
        self.entrance_repo.upsert_entrance_data(dto)

    def set_to_reenter(self, enter_info:EntranceInfoDTO):
        dto = EntranceInfoDTO(
            id= enter_info.id,
            enter_dvcd= ENTER_DVCD_REENTER,
            company_dvcd= enter_info.company_dvcd,
            seqno= enter_info.seqno+1,
            exit_yn= False
        )
        self.entrance_repo.upsert_entrance_data(dto)

    def get_latest_enter(self, login_dto):
        return self.entrance_repo.check_entered_to_entrance_info(login_dto.peer_id, login_dto.argv_company_dvcd)

    def get_latest_exit(self, login_dto):
        return self.entrance_repo.check_exit_to_entrance_info(login_dto.peer_id, login_dto.argv_company_dvcd)

class ExitMgr:
    def __init__(self
                 , entrance_repo: EntranceRepository):
        self.entrance_repo = entrance_repo

    def set_exit_true(self, enter_info_dto:EntranceInfoDTO):
        enter_info_dto.enter_dvcd = ENTER_DVCD_EXIT
        enter_info_dto.exit_yn = True
        self.entrance_repo.upsert_entrance_data(enter_info_dto)

    def set_enter_exit(self, enter_info_dto:EntranceInfoDTO):
        self.entrance_repo.update_enter_exit_true(enter_info_dto)

class ScoreMgr:
    def __init__(self,
                 score_repo: ScoreRepository,
                 common_repo: CommonRepository,
                 google_sheet_client:GoogleSheetsClient):
        self.score_repo = score_repo
        self.common_repo = common_repo
        self.google_sheet_client = google_sheet_client

    def set_score(self, score_dto):
        self.score_repo.update_nfc_exist_time_score(score_dto)

    def get_current_score(self, login_dto):
        score_info: ScoreInfoDTO = self.score_repo.get_user_current_score(login_dto.peer_id)
        if score_info is None:
            return 0
        return sum(item['score'] for item in score_info)

    def get_current_olive(self, peer_id):
        return self.score_repo.get_data_olive_info(peer_id)

    def get_exp_score(self, score_dto:ScoreInfoDTO):
        score_info = self.score_repo.get_exp_score(score_dto)
        print(f"[log] 사별, 누적 스코어 : {score_info}")
        return sum(item['score'] for item in score_info)


    def get_total_used_score(self, peer_id):
        consume_info: ConsumeInfoDTO = self.score_repo.get_total_used_score(peer_id)
        print(f"[log] consume >> {consume_info} ")
        return sum(item['used_score'] for item in consume_info)

    def set_entrance_point(self, login_dto):
        self.score_repo.update_entrance_score(login_dto.peer_id, login_dto.argv_company_dvcd)

    def validator(self, login_dto):
        self.score_repo.update_entrance_score(login_dto.peer_id, login_dto.argv_company_dvcd)

    def fetch_quiz_score(self, spreadsheet_id, range_name, company_name):
        values = self.google_sheet_client.fetch_sheet_data(spreadsheet_id, range_name)
        if not values:
            print("No data found.")
            return
        quiz_company_dvcd = self.common_repo.get_company_code(company_name).id
        self.score_repo.upsert_data_to_supabase(values, quiz_company_dvcd)

    def upload_data_to_sheet(self):
        companies = [
            (LOG_SPREADSHEET_ID, "대한통운"),
            (CJ_SPREADSHEET_ID, "제일제당"),
            (OY_SPREADSHEET_ID, "올리브영"),
            (ENM_SPREADSHEET_ID, "ENM"),
            (ONS_SPREADSHEET_ID, "올리브네트웍스")
        ]

        while True:
            for spreadsheet_id, company_name in companies:
                self.fetch_quiz_score(spreadsheet_id, SAMPLE_RANGE_NAME, company_name)
            response = self.score_repo.fetch_score_from_supabase()

            self.google_sheet_client.batch_update_sheet_data(
                TOTAL_SCORE_SPREADSHEET_ID,
                list(RankDTO.__annotations__.keys()),
                MapperUtil.convert_dicts_to_lists(response))
            time.sleep(5)  # 각 회사 처리 후 5초 대기