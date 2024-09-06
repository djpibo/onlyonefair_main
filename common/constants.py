from typing import Dict

from api.supabase.model.point import PeerInfoDTO

ENTER_DVCD_ENTRANCE = 10
ENTER_DVCD_EXIT = 11
ENTER_DVCD_REENTER = 12
ENTER_DVCD_PHOTO = 17
ENTER_DVCD_WELCOME = 18

ENTER_POINT = 50
TIME_POINT_PER_SECOND = 0.25 # 초 단위 환산 점수

BIG_ROOM_COMPANY = [5,6,7]
SMALL_ROOM_COMPANY = [8,9,13]
MIN_TIME_POINT_BIG = 120
MIN_TIME_POINT_SMALL = 45
MAX_TIME_POINT_BIG = 375
MAX_TIME_POINT_SMALL = 180

MAX_TOTAL_POINT = 3365 # 만점
PHOTO_MISSON_POINT = 200
CONSUME_PHOTO_POINT = 800
CONSUME_LUCKY_POINT = 500

# CMN_CD
QUIZ_DVCD_ROOM_QUIZ = 1
QUIZ_DVCD_SURVEY = 2
QUIZ_DVCD_NFC_ENTRANCE = 3
QUIZ_DVCD_NFC_EXIST_TIME = 4
QUIZ_DVCD_PHOTO = 14

QUIZ_SHEET_COL_INDEX_SCORE = 1
QUIZ_SHEET_COL_INDEX_ID = 3

CONSUME_PHOTO_DVCD = 15
CONSUME_LUCKY_DVCD = 16 # 럭키 드로우는 향후 일괄 집계

COMPANY_CODES = {
    "제일제당": 5,
    "대한통운": 6,
    "올리브영": 7,
    "ENM": 8,
    "커머스": 13,
    "올리브네트웍스": 9,
}

COMPANY_NAMES = {
    5: '제일제당',
    6: '대한통운',
    7: '올리브영',
    8: 'ENM',
    9: '올리브네트웍스',
    13: '커머스'
}

ENTER_EXIT_CODES = {
    '입장': 10,
    '퇴장': 11,
    '재입장': 12,
    '촬영': 17,
    '환영': 18,
    '마감': 19
}

NFC_ID_HASH_TABLE: Dict[str, PeerInfoDTO] = {
    "123456789": PeerInfoDTO(id=1, company="Company A", name="John Doe", nfc_id="123456789"),
    "987654321": PeerInfoDTO(id=2, company="Company B", name="Jane Doe", nfc_id="987654321"),
}