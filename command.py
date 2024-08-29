import math
import time
from datetime import datetime

from api.supabase.model.common import LoginDTO
from api.supabase.model.point import ConsumeInfoDTO
from api.supabase.model.presentation import ScreenDTO
from api.supabase.model.quiz import ScoreInfoDTO
from common.constants import *
from common.util import ScoreUtil, CommonUtil
from layout import Euljiro
from service.batch_score import BatchMgr
from service.common_service import CommonMgr
from service.consume_point import PointMgr
from service.nfc_service import NfcService
from service.room_stay_service import EnterMgr, ExitMgr, ScoreMgr

class Commander:
    def __init__(self, enter_mgr:EnterMgr, exit_mgr:ExitMgr, score_mgr:ScoreMgr, common_mgr:CommonMgr, nfc_mgr:NfcService,
                 eul:Euljiro, point_mgr:PointMgr, batch_mgr:BatchMgr):
        self.nfc_mgr = nfc_mgr
        self.exit_mgr = exit_mgr
        self.enter_mgr = enter_mgr
        self.score_mgr = score_mgr
        self.common_mgr = common_mgr
        self.eul = eul
        self.point_mgr = point_mgr
        self.batch_mgr = batch_mgr

    def start_nfc_polling(self, argv_arr):
        print(argv_arr)
        # Streamlit 앱 UI 구성
        while True:
            nfc_uid = self.nfc_mgr.nfc_receiver()
            self.common_mgr.count_up(nfc_uid)
            if nfc_uid is not None:

                comp_dvcd = self.common_mgr.get_cmn_cd("회사명", argv_arr[1])
                enter_dvcd = self.common_mgr.get_cmn_cd("입퇴장구분코드", argv_arr[2])
                peer_name = self.common_mgr.get_peer_name(nfc_uid)
                login_dto: LoginDTO = self.common_mgr.get_login_info(nfc_uid, comp_dvcd, peer_name)

                if enter_dvcd == ENTER_DVCD_ENTRANCE:
                    self.validate_enter(login_dto) # 입장 검증
                    self.process_enter(login_dto) # 입장 처리
                elif enter_dvcd == ENTER_DVCD_EXIT:
                    self.process_exit(login_dto) # 퇴장 처리
                else:
                    self.point_consumer(login_dto)

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
                acc_score = self.score_mgr.get_current_score(login_dto)
                used_score = self.point_mgr.get_used_score(login_dto)
                current_score = CommonUtil.get_min_time_by_company_dvcd(latest_enter_info.company_dvcd)
                comment = (f"{self.common_mgr.get_common_desc(latest_enter_info.company_dvcd)}은/는"
                           f" 최소 점수({current_score})로 퇴장 처리됐습니다.")
                scr_dto = ScreenDTO(peer_name=login_dto.peer_name, enter_dvcd_kor="입장", used_score=used_score,
                                    acc_score=acc_score+current_score, current_score=current_score, comment=comment)
                Euljiro.draw_whole(self.eul, scr_dto)

                print(f"[log] 최소 점수로 입장 처리. 클래스명: "
                      f"{self.common_mgr.get_common_desc(latest_enter_info.company_dvcd)}")

    def process_enter(self, login_dto:LoginDTO):
        reenter_enter_info = self.enter_mgr.check_exit_before(login_dto)

        if reenter_enter_info is not None:  # 퇴장 여부가 있다는 것은 재입장이라는 뜻
            print("[log] 재입장 처리 진행")
            acc_score = self.score_mgr.get_current_score(login_dto)
            used_score = self.point_mgr.get_used_score(login_dto)
            current_score = 0
            comment = (f"재입장인 경우, 입장 포인트는 없습니다.")
            scr_dto = ScreenDTO(peer_name=login_dto.peer_name, enter_dvcd_kor="재입장", used_score=used_score,
                                acc_score=acc_score + current_score, current_score=current_score, comment=comment)
            Euljiro.draw_whole(self.eul, scr_dto)
            self.enter_mgr.set_to_reenter(reenter_enter_info)
        # TODO N차 재입장 > 순번 부여로 해결 완료

        else:  # 최초 입장
            print("[log] 최초 입장 처리 진행")
            # 입장 포인트 부여
            self.score_mgr.set_entrance_point(login_dto)
            self.enter_mgr.set_to_enter(login_dto)
            acc_score = self.score_mgr.get_current_score(login_dto)
            used_score = self.point_mgr.get_used_score(login_dto)
            current_score = 50
            comment = (f"입장 포인트 50점 획득")
            scr_dto = ScreenDTO(peer_name=login_dto.peer_name, enter_dvcd_kor="입장", used_score=used_score,
                                acc_score=acc_score + current_score, current_score=current_score, comment=comment)
            Euljiro.draw_whole(self.eul, scr_dto)

    def process_exit(self, login_dto:LoginDTO):
        latest_enter_info = self.enter_mgr.get_latest_enter(login_dto)
        # 입장 안 찍고 퇴장 먼저 하는 경우
        if latest_enter_info is None:
            # TODO 단순히 여러번 찍는 경우엔 문구를 어떻게 처리? 시간 간격을 주기(연속 거래 방지) > 테스트 필요
            if CommonUtil.is_less_than_one_minute_interval(self.enter_mgr.get_latest_exit(login_dto).created_at):
                print(f"[log] 연속 거래 방지")
            else:
                print("[error] 입장 먼저 하세요.")
                acc_score = self.score_mgr.get_current_score(login_dto)
                used_score = self.point_mgr.get_used_score(login_dto)
                current_score = 0
                comment = f"{login_dto.peer_name}님! 입실 태그 먼저 찍으세요~"
                scr_dto = ScreenDTO(peer_name=login_dto.peer_name, enter_dvcd_kor="비정상 접근(퇴장)", used=used_score,
                                    acc_score=acc_score + current_score, current_score=current_score, comment=comment)
                Euljiro.draw_whole(self.eul, scr_dto)

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
            score_info_dto = ScoreInfoDTO(
                id=latest_enter_info.id, quiz_dvcd=QUIZ_DVCD_ROOM_QUIZ, company_dvcd=latest_enter_info.company_dvcd, score=0)
            bf_exp_score = self.score_mgr.get_exp_score(score_info_dto)
            if score > max_time_point - bf_exp_score:
                score = max_time_point

            # TODO 퇴장 점수 반영 > 반영 완료.
            stay_score_info = ScoreInfoDTO(
                id=login_dto.peer_id,
                quiz_dvcd=QUIZ_DVCD_NFC_EXIST_TIME,
                company_dvcd=login_dto.argv_company_dvcd,
                score=score
            )
            self.score_mgr.set_score(stay_score_info)

            # TODO 재입장 체류시간 로직 개발 > 완료 (일련번호 칼럼 추가)
            print(f"[log] latest_enter_info = {latest_enter_info}")

            self.exit_mgr.set_enter_exit(latest_enter_info)  # latest 입장 > 퇴장 여부 True
            self.exit_mgr.set_exit_true(latest_enter_info)  # 실제 퇴장 insert

            acc_score = self.score_mgr.get_current_score(login_dto)
            used_score = self.point_mgr.get_used_score(login_dto)
            current_score = score
            comment = f"입실시간 기록완료 🪄 받은 포인트 : {int(current_score)}"
            scr_dto = ScreenDTO(peer_name=login_dto.peer_name, enter_dvcd_kor="퇴장", used_score=used_score,
                                acc_score=acc_score + current_score, current_score=current_score, comment=comment)
            Euljiro.draw_whole(self.eul, scr_dto)
            print("[log] 퇴장 처리 진행")

    def start_sheet_data_batch(self):
        self.score_mgr.upload_data_to_sheet()

    # 전 사원 중에서 퇴장 여부가 False에 한해, 일괄 퇴장 처리 및 점수 부여(TODO최소시간으로??)
    def force_exit(self, login_dto=None, latest_enter_info=None):
        # TODO 최소 시간 미달시 알림 + 재입장인 경우에는 pass > 테스트를 위해 열어둠
        score = ScoreUtil.calculate_entrance_score(latest_enter_info.created_at)

        # 최초 입장인 경우, 최소 잔류 시간 검증 -> 8분 처리
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

        # TODO 화면
        # Euljiro.show_text(f"{login_dto.peer_name}님, 퇴장 완료! {score} 포인트 획득!")
        print("[log] 퇴장 처리 진행")
        # TODO 재입장 체류시간 로직 개발 > 완료 (일련번호 칼럼 추가)
        print(f"[log] latest_enter_info = {latest_enter_info}")
        self.exit_mgr.set_enter_exit(latest_enter_info)  # latest 입장 > 퇴장 여부 True
        self.exit_mgr.set_exit_true(latest_enter_info)  # 실제 퇴장 insert

    # 포인트 차감
    def point_consumer(self, login_dto):
        consumer = login_dto.peer_id

        # 1 연속 거래 방지
        if CommonUtil.is_less_than_one_minute_interval(self.point_mgr.get_latest_consume(login_dto).created_at):
            print(f"[log] 연속 거래 방지")

        # 2 누적 포인트에 기반해서 계산
        current_point = self.score_mgr.get_current_score(LoginDTO(peer_id=consumer, argv_company_dvcd=99))
        current_count = math.floor(current_point / 800)

        # 2-1 조건 검증
        if current_point > CONSUME_LUCKY_POINT:

            # 3 포인트 차감 처리
            consume_dto = ConsumeInfoDTO(id=consumer, consume_dvcd=CONSUME_PHOTO_DVCD, used_score=CONSUME_PHOTO_POINT)
            self.point_mgr.consume_point(consume_dto)

            # 4 화면 촬영권 표시
            re_point = current_point - self.score_mgr.get_total_used_score(consumer)
            print(f"[log] 총 사용 촬영권 {current_count}, 현재 잔여 촬영권 {math.floor(re_point)}")

        else:
            print(f"[log] 포인트가 부족합니다 :<")

    def start_key_polling(self, argv_arr):
        key_id = self.eul.input_id()
        comp_dvcd = self.common_mgr.get_cmn_cd("회사명", argv_arr[1])
        enter_dvcd = self.common_mgr.get_cmn_cd("입퇴장구분코드", argv_arr[2])
        peer_name = self.common_mgr.get_peer_name_by_id(key_id)
        login_dto = LoginDTO(peer_id=key_id, argv_company_dvcd=comp_dvcd, peer_name=peer_name)

        if enter_dvcd == ENTER_DVCD_ENTRANCE:
            self.validate_enter(login_dto)  # 입장 검증
            self.process_enter(login_dto)  # 입장 처리
        elif enter_dvcd == ENTER_DVCD_EXIT:
            self.process_exit(login_dto)  # 퇴장 처리
        else:
            self.point_consumer(login_dto)
        time.sleep(3)

        if key_id != "exit":  # "exit"를 입력하면 종료
            self.start_key_polling(argv_arr)
