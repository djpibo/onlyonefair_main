from api.supabase.model.quiz import ScoreInfoDTO, RankDTO
from common import constants
from common.constants import *
from common.util import MapperUtil
from config.connect import connect_supabase


class ScoreRepository:
    def __init__(self):
        self.supabase = connect_supabase()

    def upsert_data_to_supabase(self, values, quiz_company):

        data_to_upsert = [
            {
                "id": row[QUIZ_SHEET_COL_INDEX_ID],
                "quiz_dvcd": QUIZ_DVCD_ROOM_QUIZ,
                "company_dvcd": quiz_company,
                "score": row[QUIZ_SHEET_COL_INDEX_SCORE].split('/')[0].strip()
            }
            for row in values
        ]

        self.supabase.table("Score_Info").upsert(data_to_upsert, ignore_duplicates=True).execute()

    def get_user_current_score(self, peer_id):
        response = (
            self.supabase.table("Score_Info")
            .select("*")
            .eq("id", peer_id)
            .execute()
        )
        print(f"response >> {response}")
        return response.data

    def select_nfc_score(self, peer_id):
        response = (
            self.supabase.table("Score_Info")
            .select("score", count="exact")
            .eq("id", peer_id)
            .eq("quiz_dvcd", 3)
            .execute()
        )
        return MapperUtil.single_mapper(response, ScoreInfoDTO)

    # NFC 체류 시간 누적. 현재 점수 조회 후 가산
    def update_nfc_exist_time_score(self, source:ScoreInfoDTO):
        response = (
            self.supabase.table("Score_Info")
            .select("*")
            .eq("id", source.id)
            .eq("quiz_dvcd", source.quiz_dvcd)
            .eq("company_dvcd", source.company_dvcd)
            .execute()
        )
        before = MapperUtil.single_mapper(response, ScoreInfoDTO)
        if before is None:
            new_score = source.score
        else:
            new_score = source.score + before.score
        query = (
            self.supabase.table("Score_Info")
            .upsert(
                {"id": source.id,
                 "score": new_score,
                 "quiz_dvcd": source.quiz_dvcd,
                 "company_dvcd": source.company_dvcd})
            .execute()
        )

    # 입장 포인트 점수 부여
    def update_entrance_score(self, peer_id, company_dvcd):
        query = (
            self.supabase.table("Score_Info")
            .upsert(
                {"id": peer_id,
                 "score": constants.ENTER_POINT,
                 "quiz_dvcd": constants.QUIZ_DVCD_NFC_ENTRANCE,
                 "company_dvcd": company_dvcd}
                    , ignore_duplicates = True)
            .execute()
        )

    def fetch_score_from_supabase(self):
        # 실행할 SQL 쿼리
        sql_query = """
            SELECT A.id
                 , SUM(SCORE) AS TOTAL_SCORE
                 , RANK() OVER (ORDER BY SUM(SCORE) DESC) AS RANK
                 , (SELECT name FROM "Peer_Info" B WHERE B.id = A.id) name
                 , (SELECT company FROM "Peer_Info" B WHERE B.id = A.id) company
              FROM "Score_Info" A
            GROUP BY A.id
            ORDER BY SUM(SCORE) DESC
        """
        # SQL 쿼리 실행
        response = self.supabase.rpc('execute_query', {'query': sql_query}).execute()
        return MapperUtil.multi_mapper(response, RankDTO)