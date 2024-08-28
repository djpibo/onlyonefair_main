import time
import streamlit as st
import plotly.graph_objs as go

from common.constants import MAX_TOTAL_POINT

class Euljiro:

    def __init__(self):
        self.st = st
        self.c = st.container()

    @staticmethod
    def show_text(param):
        st.write(param)

    def new_draw_whole(self, scr_dto):
        placeholder = self.st.empty()

        with placeholder.container():
            st.markdown(f"<h1 style='text-align: center;'>{scr_dto.peer_name}님, {scr_dto.enter_dvcd_kor}! {scr_dto.comment} </h1>",
                        unsafe_allow_html=True)
            st.markdown("---")

            # 중간 영역
            st.markdown("<h2 style='text-align: center;'>누적 스코어</h2>", unsafe_allow_html=True)
            self.show_score(scr_dto.acc_score)

            # 하단 영역
            st.markdown("---")
            st.markdown(f"<h1 style='text-align: center;'>{scr_dto.comment}</h1>", unsafe_allow_html=True)

        time.sleep(3)
        placeholder.empty()

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