from api.supabase.model.nfc import EntranceInfoDTO
from api.supabase.model.point import ConsumeInfoDTO
from api.supabase.model.quiz import ScoreInfoDTO
from api.supabase.repo.common_repo import CommonRepository
from api.supabase.repo.entrance_repo import EntranceRepository
from api.supabase.repo.score_repo import ScoreRepository
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

    def filter_unchecked_exit(self, response, login_dto):
        if response is None:
            return None
        filtered_data = [
            row for row in response
            if row["id"] == login_dto.peer_id
               # 1-현재 입장한 클래스가 아닌 곳에서,
               and row["company_dvcd"] != login_dto.argv_company_dvcd
               # 2-퇴장을 찍고 오지 않은 경우를 반환
               and row["exit_yn"] == False
        ]
        if not filtered_data:
            return None
        return filtered_data[0]

    def check_exit_before(self, login_dto):
        return self.entrance_repo.fetch_latest_exit(login_dto.peer_id, login_dto.argv_company_dvcd)

    def filter_latest_exit(self, response, login_dto):
        if response is None:
            return None
        filtered_data = [
            record for record in response
            if record["id"] == login_dto.peer_id
            # 1-입장 클래스에서 퇴장을 한 번이라도 한 경우
               and record["company_dvcd"] == login_dto.argv_company_dvcd
               and record["exit_yn"] == True
        ]
        if filtered_data:
            # 2-일련번호를 가져오기 위함
            sorted_data = sorted(filtered_data, key=lambda x: x["seqno"], reverse=True)
            return sorted_data[0]
        else:
            return None

    def set_to_enter(self, login_dto):
        dto = EntranceInfoDTO(
            id= login_dto.peer_id,
            enter_dvcd= ENTER_DVCD_ENTRANCE,
            company_dvcd= login_dto.argv_company_dvcd,
            seqno= 1,
            exit_yn= False
        )
        self.entrance_repo.upsert_entrance_data(dto)

    def set_to_reenter(self, response):
        dto = EntranceInfoDTO(
            id= response['id'],
            enter_dvcd= ENTER_DVCD_REENTER,
            company_dvcd= response['company_dvcd'],
            seqno= response['seqno']+1,
            exit_yn= False
        )
        self.entrance_repo.upsert_entrance_data(dto)

    def get_latest_enter(self, login_dto):
        print(f"[log] 서비스 호출 : 최근 입장 데이터 가져오기")
        return self.entrance_repo.check_entered_to_entrance_info(login_dto.peer_id, login_dto.argv_company_dvcd)

    def get_latest_exit(self, login_dto):
        return self.entrance_repo.check_exit_to_entrance_info(login_dto.peer_id, login_dto.argv_company_dvcd)

    def validate_if_full(self, login_dto):
        response = self.score_repo.get_exp_score(
            ScoreInfoDTO(id=login_dto.peer_id,
                         quiz_dvcd=QUIZ_DVCD_NFC_EXIST_TIME,
                         company_dvcd=login_dto.argv_company_dvcd,
                         score=99))
        bf_exp_score = sum(item['score'] for item in response)
        return bf_exp_score >= CommonUtil.get_max_time_by_company_dvcd(login_dto.argv_company_dvcd)

    def validate_if_fulled(self, response, login_dto):
        print("[log] 서비스 호출 : 체류시간이 상한 포인트을 넘겼는지 검증")
        print(f"[log] respnse > {response}")
        total_score = sum(
            record['score']
            for record in response
            if record['id'] == login_dto.peer_id
            and record['quiz_dvcd'] == QUIZ_DVCD_NFC_EXIST_TIME
            and record['company_dvcd'] == login_dto.argv_company_dvcd
        )
        return total_score >= CommonUtil.get_max_time_by_company_dvcd(login_dto.argv_company_dvcd)

    def get_entrance_data(self, login_dto):
        if login_dto is None:
            return None
        return self.entrance_repo.get_entrance_data_by_id(login_dto.peer_id).data or None

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
                 common_repo: CommonRepository):
        self.score_repo = score_repo
        self.common_repo = common_repo

    def set_score(self, score_dto):
        return self.score_repo.update_nfc_exist_time_score(score_dto)

    def get_current_point(self, login_dto):
        score_info: ScoreInfoDTO = self.score_repo.get_user_current_point(login_dto.peer_id)
        if score_info is None:
            return 0
        return sum(item['score'] for item in score_info)

    def sum_current_point(self, response):
        if response:
            return sum(item['score'] for item in response)
        return 0

    def get_current_olive(self, peer_id):
        return self.score_repo.get_data_olive_info(peer_id)

    def get_exp_score(self, score_dto:ScoreInfoDTO):
        score_info = self.score_repo.get_exp_score(score_dto)
        return sum(item['score'] for item in score_info)

    def get_total_used_score(self, peer_id):
        consume_info: ConsumeInfoDTO = self.score_repo.get_total_used_score(peer_id)
        print(f"[log] consume >> {consume_info} ")
        return sum(item['used_score'] for item in consume_info)

    def set_entrance_point(self, login_dto):
        self.score_repo.update_entrance_score(login_dto.peer_id, login_dto.argv_company_dvcd)

    def validator(self, login_dto):
        self.score_repo.update_entrance_score(login_dto.peer_id, login_dto.argv_company_dvcd)