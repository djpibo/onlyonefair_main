import asyncio
from api.supabase.model import LoginDTO
from api.supabase.repo.common_repo import CommonRepository
from api.supabase.repo.peer_repo import PeerRepository
from common.constants import *
from config.connect import connect_redis
from threading import local


class CommonMgr:
    def __init__(self, common_repo: CommonRepository, peer_repo: PeerRepository):
        self.common_repo = common_repo
        self.peer_repo = peer_repo
        self.redis = None
        self.thread_local = local()

    def get_common_desc(self, company_dvcd):
        return COMPANY_NAMES.get(company_dvcd)

    def count_up(self, _id):
        self.common_repo.insert_tag_count(_id)

    def validate_teacher(self, nfc_id):
        if self.peer_repo.check_if_teacher(nfc_id) is None:
            return True

    def login_setter(self, argv1, argv2, nfc_uid):
        comp_dvcd = COMPANY_CODES.get(argv1)
        enter_dvcd = ENTER_EXIT_CODES.get(argv2)
        response = self.peer_repo.fetch_peer_id_from_supabase(nfc_uid)
        peer_company = response.company
        peer_name = response.name
        peer_id = response.id
        return LoginDTO(peer_id=peer_id, argv_company_dvcd=comp_dvcd, peer_name=peer_name, peer_company=peer_company,
                        enter_dvcd=enter_dvcd)

    async def set_login_info(self, _id):
        self.redis = await connect_redis()
        try:
            #1 redis
            company_str, enter_str = await asyncio.gather(
                self.get_redis_value('company'),
                self.get_redis_value('enter')
            )

            if company_str is None or enter_str is None:
                raise ValueError("[WARN] Company or enter string not available from Redis.")

            #2 constant
            company_code = COMPANY_CODES.get(company_str)
            enter_code = ENTER_EXIT_CODES.get(enter_str)

            if company_code is None or enter_code is None:
                raise ValueError("[WARN] Invalid company code or enter code from constants")

            #3 DB
            response = await self.fetch_peer_info(_id)
            if response is None:
                raise ValueError(f"[WARN] Failed to retrieve peer info for ID {_id}")

            data_dict = {
                "peer_id": response.id,
                "peer_name": response.name,
                "peer_company": response.company,
                "company_str": company_str,
                "company_code": company_code,
                "enter_str": enter_str,
                "enter_code": enter_code,
            }

            self.thread_local.data = data_dict

            print(f"THREAD LOCAL DATA >> {self.thread_local.data}")

        except Exception as e:
            print(f"[WARN] Error gathering data: {e}")
            return None

    async def get_redis_value(self, key):
        try:
            value = await self.redis.get(key)
            if value is None:
                raise ValueError(f"[WARN] Key '{key}' not found in Redis.")
            return value.decode('utf-8')
        except ValueError as e:
            print(f"[WARN] Error fetching '{key}' from Redis: {e}")
            return None

    async def fetch_peer_info(self, _id):
        try:
            response = await self.peer_repo.fetch_peer_info_by_id(_id)
            if response is None:
                raise ValueError(f"[WARN] No peer found with ID {_id}")
            return response
        except Exception as e:
            print(f"[WARN] Error fetching peer info with ID {_id}: {e}")
            return None
