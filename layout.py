import streamlit as st

class Euljiro:

    @staticmethod
    def writer(text):
        st.markdown("""
            <style>
            .fixed-header {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                background-color: white;
                padding: 10px;
                border-bottom: 1px solid #ddd;
                z-index: 1000;
            }
            .content {
                margin-top: 60px;  /* 상단 고정 요소의 높이만큼 마진을 추가합니다 */
            }
            </style>
            <div class="fixed-header">
                <h3>{nm}님 입장하셨습니다.</h3>
            </div>
            <div class="content">
        """, unsafe_allow_html=True)

        # 나머지 콘텐츠
        st.write("여기에 나머지 콘텐츠를 추가합니다.")

        # HTML 종료 태그 추가
        st.markdown("</div>", unsafe_allow_html=True)