from api.supabase.model import ConsumeInfoDTO
from api.supabase.model import ScoreInfoDTO
from common import constants
from common.constants import *
from common.util import MapperUtil, CommonUtil
from config.connect import connect_supabase


class ScoreRepository:
    def __init__(self):
        self.supabase = connect_supabase()

    def get_user_current_point(self, peer_id):
        response = (
            self.supabase.table("Score_Info")
            .select("*")
            .eq("id", peer_id)
            .execute()
        )
        if response.data is None:
            return None
        return response.data

    # NFC 체류 시간 누적. 현재 점수 조회 후 가산
    def update_nfc_exist_time_score(self, source: ScoreInfoDTO):
        response = (
            self.supabase.table("Score_Info")
            .select("*")
            .eq("id", source.id)
            .eq("quiz_dvcd", source.quiz_dvcd)
            .eq("company_dvcd", source.company_dvcd)
            .execute()
        )
        before = MapperUtil.single_mapper(response, ScoreInfoDTO)
        # 최초 퇴장인 경우
        if before is None:
            new_score = source.score
        # N차 퇴장인 경우엔 합산
        else:
            new_score = min(source.score + before.score, CommonUtil.get_max_time_by_company_dvcd(source.company_dvcd))
        query = (
            self.supabase.table("Score_Info")
            .upsert(
                {"id": source.id,
                 "score": new_score,
                 "quiz_dvcd": source.quiz_dvcd,
                 "company_dvcd": source.company_dvcd})
            .execute()
        )
        return query

    # 입장 포인트 점수 부여
    def update_entrance_score(self, peer_id, company_dvcd):
        (self.supabase.table("Score_Info")
         .upsert(
            {"id": peer_id,
             "score": constants.ENTER_POINT,
             "quiz_dvcd": constants.QUIZ_DVCD_NFC_ENTRANCE,
             "company_dvcd": company_dvcd}, ignore_duplicates=True)
         .execute())

    def insert_used_point(self, consume_info: ConsumeInfoDTO):
        (self.supabase.table("Consume_Info")
         .insert({"id": consume_info.id,
                  "consume_dvcd": consume_info.consume_dvcd,
                  "used_score": consume_info.used_score}
                 )
         .execute())

    def get_exp_score(self, score_dto: ScoreInfoDTO):
        return (self.supabase.table("Score_Info")
                .select("score")
                .eq("id", score_dto.id)
                .eq("company_dvcd", score_dto.company_dvcd)
                .eq("quiz_dvcd", score_dto.quiz_dvcd)
                .execute()).data

    def get_used_point_by_id(self, peer_id):
        return self.supabase.table("Consume_Info").select("*").eq("id", peer_id).execute().data

    def get_data_by_id(self, peer_id):
        return self.supabase.table("Score_Info").select("*").eq("id", peer_id).execute().data

    def update_mission_score(self, peer_id):
        (self.supabase.table("Score_Info")
         .upsert(
            {"id": peer_id,
             "score": PHOTO_MISSION_POINT,
             "quiz_dvcd": QUIZ_DVCD_PHOTO,
             "company_dvcd": ENTER_EXIT_CODES.get('포토미션')}, ignore_duplicates=True)
         .execute())
