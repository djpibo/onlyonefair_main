import sys

from injector import Injector
from command import Commander
from inject_module import ChungMuro

def main():

    # Injector(DI) 설정
    injector = Injector([ChungMuro()])
    commander = injector.get(Commander)

    if len(sys.argv) == 1: # 알바생을 위한 포인트 차감
        commander.point_consumer()

    if len(sys.argv) == 2: # 구글 시트 연동 배치 수행
        commander.start_sheet_data_batch()

    if len(sys.argv) == 3: # 각 클래스 입장
        commander.start_nfc_polling(sys.argv)

    if len(sys.argv) == 4: # 강제 종료
        commander.start_key_polling(sys.argv)

    if len(sys.argv) == 5: # 강제 종료
        commander.force_exit()


if __name__ == "__main__":
    main()
