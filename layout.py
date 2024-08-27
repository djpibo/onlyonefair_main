import time

import streamlit as st
import plotly.graph_objs as go

from api.supabase.model.presentation import ScreenDTO
from common.constants import MAX_TOTAL_POINT

class Euljiro:

    def __init__(self):
        self.st = st
        self.c = st.container()

    @staticmethod
    def init_layout(param):
        st.set_page_config(
            page_title=f"{param}",  # 페이지 제목
            page_icon=":bar_chart:",  # 페이지 아이콘
            layout="wide"  # 레이아웃을 wide로 설정
        )

    @staticmethod
    def show_text(param):
        st.write(param)

    # 재사용 가능한 컴포넌트 함수 정의
    @staticmethod
    def reusable_component(placeholder, title, content, border_color="blue"):
        with placeholder.container():
            st.markdown(f"<h2 style='color:{border_color};'>{title}</h2>", unsafe_allow_html=True)
            st.write(content)

    def new_draw_whole(self, scr_dto):
        placeholder = self.st.empty()

        # Replace the chart with several elements:
        with placeholder.container():
            st.markdown(f"<h1 style='text-align: center;'>{scr_dto.peer_name}님, {scr_dto.enter_dvcd_kor}! </h1>",
                        unsafe_allow_html=True)
            st.markdown("---")

            # 중간 영역
            st.markdown("<h2 style='text-align: center;'>누적 스코어</h2>", unsafe_allow_html=True)
            self.show_score(scr_dto.acc_score)

            # 하단 영역
            # st.markdown("---")
            # st.markdown(f"<h1 style='text-align: center;'>재입장인 경우 입장 포인트는 제공되지 않음</h1>", unsafe_allow_html=True)

        time.sleep(3)
        placeholder.empty()

    def draw_whole(self, scr_dto:ScreenDTO):
        # 상단 영역
        c = self.c
        c.empty()
        st.markdown(f"<h1 style='text-align: center;'>{scr_dto.enter_dvcd_kor} {scr_dto.peer_name}</h1>", unsafe_allow_html=True)
        st.markdown("---")

        # 중간 영역
        # middle_placeholder.markdown("<h2 style='text-align: center;'>누적 스코어</h2>", unsafe_allow_html=True)
        self.show_score(110)

        # 하단 영역
        st.markdown("---")
        st.markdown(f"<h1 style='text-align: center;'></h1>", unsafe_allow_html=True)

    @staticmethod
    def show_notify(peer_name, enter_kor):
        pass


    def show_score(self, acc_score):

        # # 비중 계산
        # progress_percent = int((current_score / MAX_TOTAL_POINT) * 100)
        #
        # progress = st.progress(0) # 0점에서 시작
        # # progress.header(f"현재 누적 점수 : {current_score}")
        # for i in range(progress_percent):
        #     time.sleep(0.05)
        #     progress.progress(i + 1)

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

        # # Plotly 막대 그래프 생성
        # fig = go.Figure(go.Bar(
        #     x=[progress_percent],  # 비중을 x축 값으로 설정
        #     y=['Progress'],  # y축은 단일 값 'Progress'로 설정
        #     orientation='h',  # 가로 방향으로 막대 그래프 설정
        #     marker=dict(color='blue'),  # 막대 색상 설정
        #     text=f'{progress_percent:.2f}%',  # 비중 텍스트
        #     textposition='inside',  # 텍스트 위치를 막대 내부로 설정
        #     width=0.4  # 막대의 두께 설정
        # ))
        #
        # # 레이아웃 조정
        # fig.update_layout(
        #     xaxis=dict(range=[0, 100], title=''),  # x축 범위를 0-100으로 설정
        #     yaxis=dict(title=''),  # y축 제목을 비워둡니다
        #     title=f'현재 누적 점수 / 최고 획득 가능 점수: {current_score} / {MAX_TOTAL_POINT}',  # 그래프 제목
        #     showlegend=False  # 범례 숨기기
        # )
        #
        # # Streamlit 앱에 그래프 출력
        # st.plotly_chart(fig)