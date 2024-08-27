import time

from api.supabase.model.common import LoginDTO
from api.supabase.model.quiz import ScoreInfoDTO
from common.constants import *
from common.util import ScoreUtil, CommonUtil
from layout import Euljiro
from service.common_service import CommonMgr
from service.nfc_service import NfcService
from service.room_stay_service import EnterMgr, ExitMgr, ScoreMgr


class Commander:
    def __init__(self,
                 enter_mgr:EnterMgr,
                 exit_mgr:ExitMgr,
                 score_mgr:ScoreMgr,
                 common_mgr:CommonMgr,
                 nfc_mgr:NfcService):
        self.nfc_mgr = nfc_mgr
        self.exit_mgr = exit_mgr
        self.enter_mgr = enter_mgr
        self.score_mgr = score_mgr
        self.common_mgr = common_mgr

    def start_nfc_polling(self, argv_arr):
        print(argv_arr)
        #Euljiro.init_layout_1(argv_arr[1])
        Euljiro.size_layout()
        # Streamlit 앱 UI 구성
        while True:
            nfc_uid = self.nfc_mgr.nfc_receiver()

            if nfc_uid is not None:

                comp_dvcd = self.common_mgr.get_cmn_cd("회사명", argv_arr[1])
                enter_dvcd = self.common_mgr.get_cmn_cd("입퇴장구분코드", argv_arr[2])
                peer_name = self.common_mgr.get_peer_name(nfc_uid)
                login_dto: LoginDTO = self.common_mgr.get_login_info(nfc_uid, comp_dvcd, peer_name)

                if enter_dvcd == ENTER_DVCD_ENTRANCE:
                    self.validate_enter(login_dto) # 입장 검증
                    self.process_enter(login_dto) # 입장 처리
                else:
                    self.process_exit(login_dto) # 퇴장 처리

            time.sleep(1)

    def validate_enter(self, login_dto:LoginDTO):
        latest_enter_info = self.enter_mgr.get_unchecked_exit(login_dto)
        if latest_enter_info is not None:  # 퇴장을 찍고 오지 않은 경우 이전 부스 입장 내역이 남아 있다.
            if ScoreUtil.check_min_stay_time(latest_enter_info):  # 시간이 모자란 경우
                # 다시 원래 부스로 돌아가기 or 0점 처리 입장
                pass
                # TODO GUI에서 선택값 받기

            else:  # 그래도 시간은 채운 경우, 퇴장 처리 후 최소 점수로 입장
                # 1-퇴장 처리(입장(또는 재입장) => True, 퇴장 insert)
                self.exit_mgr.set_enter_exit(latest_enter_info)
                self.exit_mgr.set_exit_true(latest_enter_info)
                # 2-최소 점수 받기 (그리고 입장)
                set_to_score_info = ScoreInfoDTO(
                    id=login_dto.peer_id,
                    quiz_dvcd=QUIZ_DVCD_NFC_EXIST_TIME,
                    company_dvcd=latest_enter_info.company_dvcd,
                    score=CommonUtil.get_min_time_by_company_dvcd(latest_enter_info.company_dvcd)
                )
                self.score_mgr.set_score(set_to_score_info)

                # TODO GUI
                Euljiro.show_text(f"{self.common_mgr.get_common_desc(latest_enter_info.company_dvcd)}은/는 최소 점수로 입장 처리됐습니다.")

                print(f"[log] 최소 점수로 입장 처리. 클래스명: "
                      f"{self.common_mgr.get_common_desc(latest_enter_info.company_dvcd)}")

    def process_enter(self, login_dto:LoginDTO):
        reenter_enter_info = self.enter_mgr.check_exit_before(login_dto)

        if reenter_enter_info is not None:  # 퇴장 여부가 있다는 것은 재입장이라는 뜻
            print("[log] 재입장 처리 진행")
            Euljiro.show_text(f"{login_dto.peer_name}님 재입장입니다. 입장 포인트는 부여되지 않습니다.")
            Euljiro.draw_progress_bar(self.score_mgr.get_current_score(login_dto))
            self.enter_mgr.set_to_reenter(reenter_enter_info)
        # TODO N차 재입장 > 순번 부여로 해결 완료

        else:  # 최초 입장
            print("[log] 최초 입장 처리 진행")
            Euljiro.init_layout(f"{login_dto.peer_name}님 입장! 입장 포인트(50p) 획득!",
                                (self.score_mgr.get_current_score(login_dto)))
            # 입장 포인트 부여
            self.score_mgr.set_entrance_point(login_dto)
            self.enter_mgr.set_to_enter(login_dto)

    def process_exit(self, login_dto:LoginDTO):
        latest_enter_info = self.enter_mgr.get_latest_enter(login_dto)
        # 입장 안 찍고 퇴장 먼저 하는 경우
        if latest_enter_info is None:
            # TODO 단순히 여러번 찍는 경우엔 문구를 어떻게 처리? 시간 간격을 주기(연속 거래 방지) > 테스트 필요
            if CommonUtil.is_less_than_one_minute_interval(self.enter_mgr.get_latest_exit(login_dto).created_at):
                print(f"[log] 연속 거래 방지")
            else:
                Euljiro.show_text(f"{login_dto.peer_name}님! 입실 태그 먼저 찍으세요~")
                print("[error] 입장 먼저 하세요.")

        # 정상 퇴장 진행
        else:
            # TODO 최소 시간 미달시 알림 + 재입장인 경우에는 pass > 테스트를 위해 열어둠
            score = ScoreUtil.calculate_entrance_score(latest_enter_info.created_at)

            # 최초 입장인 경우, 최소 잔류 시간 검증
            if latest_enter_info.enter_dvcd == ENTER_DVCD_ENTRANCE:
                min_time_point = CommonUtil.get_min_time_by_company_dvcd(latest_enter_info.company_dvcd)
                if min_time_point is not None and score < min_time_point:
                    # TODO GUI (퇴장 허용 or 0점 퇴장)
                    Euljiro.show_text(f"{login_dto.peer_name}님! 아직 최소 시간을 채우지 못했습니다."
                                      f" {format(ScoreUtil.calculate_time_by_score(min_time_point, score))}가 더 필요해요~")
                    print("[error] 최소 시간 미달입니다. {} 필요"
                          .format(ScoreUtil.calculate_time_by_score(min_time_point, score)))

            # 상한 시간 지정
            max_time_point = CommonUtil.get_max_time_by_company_dvcd(latest_enter_info.company_dvcd)
            if max_time_point is not None and score > max_time_point:
                score = max_time_point

            # TODO 퇴장 점수 반영 > 반영 완료.
            stay_score_info = ScoreInfoDTO(
                id=login_dto.peer_id,
                quiz_dvcd=QUIZ_DVCD_NFC_EXIST_TIME,
                company_dvcd=login_dto.argv_company_dvcd,
                score=score
            )
            self.score_mgr.set_score(stay_score_info)

            Euljiro.show_text(f"{login_dto.peer_name}님, 퇴장 완료! {score} 포인트 획득!")
            print("[log] 퇴장 처리 진행")
            # TODO 재입장 체류시간 로직 개발 > 완료 (일련번호 칼럼 추가)
            print(f"[log] latest_enter_info = {latest_enter_info}")
            self.exit_mgr.set_enter_exit(latest_enter_info)  # latest 입장 > 퇴장 여부 True
            self.exit_mgr.set_exit_true(latest_enter_info)  # 실제 퇴장 insert

    def start_sheet_data_batch(self):
        self.score_mgr.upload_data_to_sheet()