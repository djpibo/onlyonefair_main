import os
import time
from datetime import datetime
from pathlib import Path
from xmlrpc.client import DateTime

from PIL import Image

import streamlit as st
import plotly.graph_objs as go

from api.supabase.model.presentation import ScreenDTO
from common.constants import MAX_TOTAL_POINT

class Euljiro:

    def __init__(self):
        self.st = st
        self.c = st.container()
        self.placeholder = self.st.empty()

    @staticmethod
    def show_text(param):
        st.write(param)

    def draw_whole(self, scr_dto:ScreenDTO):
        self.clean_whole()
        with self.placeholder.container():
            self.st.markdown(f"<h1 style='text-align: center;'>🛎️</h1>"
                             f"<h1 style='text-align: center;'>{scr_dto.peer_name}님, {scr_dto.enter_dvcd_kor}️</h1>"
                        # f"<h2 style='text-align: center;margin-bottom: 5px;padding: 5px 0;'>📣</h2>"
                        f"<h2 style='text-align: center;margin-bottom: 5px;padding: 5px 0;'>{scr_dto.comment}</h2>",
                        unsafe_allow_html=True)
            self.st.markdown("---")
            # self.camera_counter(scr_dto)

            # 중간 영역
            self.st.markdown(f"<h2 style='text-align: center;margin-bottom: 5px;padding: 5px 0;'> "
                             f"🏆 현재 누적 포인트 : {int(scr_dto.acc_score)} (+{int(scr_dto.current_score)}) </h2> "
                        , unsafe_allow_html=True)
            # self.show_score(scr_dto.acc_score)

    def clean_whole(self):
        self.placeholder.empty()

    def show_score(self, acc_score):

        # 예시 데이터
        data = {
            'Subcategory 1': acc_score,
            'Subcategory 2': MAX_TOTAL_POINT
        }
        # 서브 카테고리 색상 설정
        colors = {
            'Subcategory 1': '#4682B4',
            'Subcategory 2': 'gray'
        }

        # Plotly 막대 그래프 생성
        fig = go.Figure()

        # 데이터 추가
        for subcategory, value in data.items():
            fig.add_trace(go.Bar(
                x=[value],  # 각 하위 항목의 값
                name=subcategory,  # 하위 항목의 이름
                orientation='h',  # 가로 방향으로 막대 그래프 설정
                text=f'{value}',  # 막대에 표시할 텍스트
                marker=dict(color=colors[subcategory]),  # 서브 카테고리 색상 설정
                textposition='inside',  # 텍스트 위치를 막대 내부로 설정
                textfont=dict(size=50)  # 텍스트 폰트 크기 설정
            ))

        # 레이아웃 조정
        fig.update_layout(
            barmode='stack',  # 스택형 막대 그래프 설정
            xaxis=dict(
                showticklabels=False,  # x축의 숫자 레이블 숨기기
                showline=False,  # x축 선 숨기기
                showgrid=False  # x축 그리드 숨기기
            ),
            yaxis=dict(
                showticklabels=False,  # y축의 숫자 레이블 숨기기
                showline=False,  # y축 선 숨기기
                showgrid=False  # y축 그리드 숨기기
            ),
            #title='현재 누적 점수',  # 그래프 제목 설정
            height=300,  # 그래프 높이 설정 (픽셀 단위)
            width=1600,  # 그래프 너비 설정 (픽셀 단위)
            showlegend=False,  # 범례 숨기기
            font = dict(size=200)  # 전체 폰트 크기 설정
        )

        # Streamlit 앱에 그래프 출력
        self.st.plotly_chart(fig)

    @staticmethod
    def add_fullscreen_wave_css():
        placeholder = st.empty()
        with placeholder.container():
            wave_css = """
            <style>
            body, html {
                margin: 0;
                padding: 0;
                width: 100%;
                height: 100%;
                overflow: hidden;
            }
    
            .wave-container {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                overflow: hidden;
                z-index: -1;
            }
    
            .wave {
                position: absolute;
                width: 200%;
                height: 100%;
                background: linear-gradient(45deg, #00f, #08f, #0af, #00f);
                opacity: 0.7;
                animation: wave-animation 10s infinite linear;
                top: -75px;
                left: -100%;
                transform: rotate(0deg);
            }
    
            .wave:nth-child(2) {
                animation: wave-animation 12s infinite linear reverse;
                opacity: 0.5;
            }
    
            .wave:nth-child(3) {
                animation: wave-animation 14s infinite linear;
                opacity: 0.3;
            }
    
            @keyframes wave-animation {
                0% {
                    transform: translateX(0) translateY(0) rotate(0deg);
                }
                50% {
                    transform: translateX(25%) translateY(10px) rotate(-2deg);
                }
                100% {
                    transform: translateX(50%) translateY(0) rotate(0deg);
                }
            }
            </style>
            <div class="wave-container">
                <div class="wave"></div>
                <div class="wave"></div>
                <div class="wave"></div>
            </div>
            """
            placeholder.markdown(wave_css, unsafe_allow_html=True)

    def camera_counter(self, scr_dto):
        current_dir = Path(__file__).parent
        live_camera = current_dir / "src" / "live_camera.png"
        dead_camera = current_dir / "src" / "dead_camera.png"
        live_img = Image.open(live_camera).resize((70, 70))
        dead_img = Image.open(dead_camera).resize((70, 70))

        total_count = int(scr_dto.acc_score/800)
        dead_count = int(scr_dto.used_score/800)
        live_count = total_count-dead_count

        # 이미지 리스트 생성
        live_images = [live_img] * live_count
        dead_images = [dead_img] * dead_count

        # Streamlit 화면에 이미지 나열
        for img in live_images:
            self.st.image(img, use_column_width=False)
        for img in dead_images:
            self.st.image(img, use_column_width=False)

    def reset_key(self):
        """텍스트 입력 필드의 키를 초기화."""
        self.st.session_state['emp_id_key'] = None

    def handle_input(self, emp_id):
        """사번 입력값을 처리."""
        if emp_id:
            # 입력을 처리한 후 키를 초기화하여 중복 방지
            self.reset_key()
            return emp_id
        return None

    def input_id(self):
        self.clean_whole()
        # 세션 상태를 관리하기 위해 st.session_state 사용
        return self.placeholder.text_input("사번을 입력하세요:", key="emp_id_key")
