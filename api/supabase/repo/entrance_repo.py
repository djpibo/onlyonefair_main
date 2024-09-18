from api.supabase.model import EntranceInfoDTO
from common import constants
from common.constants import ENTER_DVCD_EXIT, ENTER_DVCD_ENTRANCE, ENTER_DVCD_REENTER
from common.util import MapperUtil
from config.connect import connect_supabase


class EntranceRepository:
    def __init__(self):
        self.supabase = connect_supabase()

    def update_enter_exit_true(self, entrance_info_dto: EntranceInfoDTO):
        (self.supabase.table("Entrance_Info")
         .update({"exit_yn": True})
         .eq("id", entrance_info_dto.id)
         .eq("company_dvcd", entrance_info_dto.company_dvcd)
         .eq("enter_dvcd", entrance_info_dto.enter_dvcd)
         .eq("seqno", entrance_info_dto.seqno)
         .execute())

    def upsert_first_enter(self, _dto: EntranceInfoDTO):

        data_to_upsert = {
            "id": _dto.id,
            "company_dvcd": _dto.company_dvcd,
            "enter_dvcd": ENTER_DVCD_ENTRANCE,
            "seqno": 1,
            "exit_yn": False
        }
        self.supabase.table("Entrance_Info").upsert([data_to_upsert], ignore_duplicates=True).execute()

    def upsert_re_enter(self, _dto: EntranceInfoDTO):

        data_to_upsert = {
            "id": _dto.id,
            "company_dvcd": _dto.company_dvcd,
            "enter_dvcd": ENTER_DVCD_REENTER,
            "seqno": _dto.seqno,
            "exit_yn": _dto.exit_yn
        }
        self.supabase.table("Entrance_Info").upsert([data_to_upsert]).execute()

    def upsert_entrance_data(self, entrance_info_dto: EntranceInfoDTO):

        data_to_upsert = [
            {
                "id": entrance_info_dto.id,
                "company_dvcd": entrance_info_dto.company_dvcd,
                "enter_dvcd": entrance_info_dto.enter_dvcd,
                "seqno": entrance_info_dto.seqno,
                "exit_yn": entrance_info_dto.exit_yn
            }
        ]
        query = self.supabase.table("Entrance_Info")
        if entrance_info_dto.enter_dvcd == constants.ENTER_DVCD_ENTRANCE:
            query = query.upsert(data_to_upsert, ignore_duplicates=True)
        else:
            query = query.upsert(data_to_upsert)
        query.execute()

    # 가장 최근에 입장한 정보를 가져오기(시간 계산) + 퇴장-검증에서도 사용
    def check_entered_to_entrance_info(self, peer_id, company_dvcd):
        response = (
            self.supabase.table("Entrance_Info")
            .select("*")
            .eq("id", peer_id)
            .eq("company_dvcd", company_dvcd)
            .eq("exit_yn", False)  # 퇴장 전에는 False 이므로
            .in_("enter_dvcd", [10, 12])  # 입장 or 재입장
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )
        return MapperUtil.single_mapper(response, EntranceInfoDTO)

    # 연속 퇴장 여부 확인
    def check_exit_to_entrance_info(self, peer_id, company_dvcd):
        response = (
            self.supabase.table("Entrance_Info")
            .select("*")
            .eq("id", peer_id)
            .eq("company_dvcd", company_dvcd)
            .eq("exit_yn", True)
            .eq("enter_dvcd", ENTER_DVCD_EXIT)
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )
        return MapperUtil.single_mapper(response, EntranceInfoDTO)

    def get_entrance_data_by_id(self, _id):
        return self.supabase.table("Entrance_Info").select("*").eq("id", _id).execute() or None
