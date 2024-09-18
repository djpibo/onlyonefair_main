from datetime import datetime
import pytz
from common.constants import *
from typing import TypeVar, Type, List, Optional
from pydantic import BaseModel
from postgrest.base_request_builder import APIResponse

class CommonUtil:
    @staticmethod
    def get_min_time_by_company_dvcd(company_dvcd):
        return MIN_TIME_POINT_BIG if company_dvcd in BIG_ROOM_COMPANY else MIN_TIME_POINT_SMALL

    @staticmethod
    def get_max_time_by_company_dvcd(company_dvcd):
        print("[INFO] common util : 클래스별 최대 포인트 조회")
        return MAX_TIME_POINT_BIG if company_dvcd in BIG_ROOM_COMPANY else MAX_TIME_POINT_SMALL

    @staticmethod
    def calculate_time_interval(given_time):
        print("[INFO] common util : 체류 시간 계산")
        seoul_tz = pytz.timezone('Asia/Seoul')
        current_time = datetime.now(seoul_tz)
        return int(current_time.timestamp() - given_time.timestamp())

    @staticmethod
    def is_less_than_one_minute_interval(given_time):
        print("[INFO] common util : 연속 거래 방지")
        if given_time is None:
            return False
        return CommonUtil.calculate_time_interval(given_time.created_at) < 60

class ScoreUtil:
    def __init__(self):
        pass

    @staticmethod
    def calculate_entrance_score(target_time):
        print("[log] 공통 유틸 : 체류 시간 계산하기")
        seoul_tz = pytz.timezone('Asia/Seoul')
        current_time = datetime.now(seoul_tz)
        time_difference = int(current_time.timestamp() - target_time.timestamp())
        return time_difference * TIME_POINT_PER_SECOND

    @staticmethod
    def calculate_time_by_score(source_score, user_score):
        remain_score = source_score - user_score
        print(remain_score)
        remain_time_sec = remain_score / TIME_POINT_PER_SECOND
        print(remain_time_sec)
        return f"{int(remain_time_sec/60)}분 {int(remain_time_sec%60)}초"

    @staticmethod
    def check_min_stay_time(response):
        print(f"[log] 경과 시간 확인 {ScoreUtil.calculate_entrance_score(response.created_at)}")
        print(f"[log] 각 사 최소 시간 {CommonUtil.get_min_time_by_company_dvcd(response.company_dvcd)}")

        # 각 사 최소체류시간보다 오래 버틴 경우, true
        return (ScoreUtil.calculate_entrance_score(response.created_at)
                > CommonUtil.get_min_time_by_company_dvcd(response.company_dvcd))

class MapperUtil:
    def __init__(self):
        pass
    # TypeVar로 DTO 클래스 타입을 정의
    T = TypeVar('T', bound=BaseModel)

    @staticmethod
    def multi_mapper(response: APIResponse, dto_class: Type[T]) -> Optional[List[T]]:
        return response.data
        # if not data:
        #     print(f"[log] data none? test !")
        #     return None
        # return [dto_class(**item) for item in data]

    @staticmethod
    def single_mapper(response: APIResponse, dto_class: Type[T]) -> Optional[T]:
        if not response.data:
            return None
        if len(response.data) > 1:
            raise ValueError("Expected a single result, but multiple records were found.")
        return dto_class(**response.data[0])