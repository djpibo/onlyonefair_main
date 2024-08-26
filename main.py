import sys

import streamlit as st
from injector import Injector
from command import Commander
from inject_module import ChungMuro

def main():

    # Injector(DI) 설정
    injector = Injector([ChungMuro()])
    commander = injector.get(Commander)

    # Streamlit 앱 UI 구성
    st.set_page_config(page_title="CJ 올리브영", layout="wide")

    if len(sys.argv) != 3:
        print("Usage: main.py <quiz_company> <enter_dvcd>")
        #sys.exit(1)
        commander.start_sheet_data_batch()

    commander.start_nfc_polling(sys.argv)

if __name__ == "__main__":
    main()
