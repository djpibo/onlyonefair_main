import httpx
from flask import Flask, render_template
from flask_socketio import SocketIO

from injector import Injector

from api.supabase.model.presentation import ScreenDTO
from command import Commander
from inject_module import ChungMuro

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")  # CORS 설정

injector = Injector([ChungMuro()])
commander = injector.get(Commander)

@app.route('/')
def index():
    return render_template('index.html')
    # return render_template('index.html', scr_dto=scr_dto)

@socketio.on('nfc_data')
def handle_nfc_data(response):
    print("[log] NFC 데이터 수신:", response)
    try:
        scr_dto: ScreenDTO = commander.start_card_polling(response['data'])
        if scr_dto.peer_name == "운영진":
            print(f"[log] 운영진 렌더링 시작.. ")
            socketio.emit('polling_result', {
                'comment': scr_dto.comment,
                'acc_score': '',
                'current_score': '☺︎',
                'photo': '♾️',
                'peer_name': scr_dto.peer_name,
                'peer_company': scr_dto.peer_company,
                'enter_dvcd': '',
            })
        else:
            # 클라이언트에 반환된 결과를 전송
            socketio.emit('polling_result', {
                'comment': scr_dto.comment,
                'acc_score': int(scr_dto.acc_score),
                'current_score': int(scr_dto.current_score),
                'photo': int((scr_dto.acc_score - scr_dto.used_score)/800),
                'peer_name': scr_dto.peer_name,
                'peer_company': scr_dto.peer_company,
                'enter_dvcd': scr_dto.enter_dvcd_kor,
                'require_time': scr_dto.require_time,
            })

    # HTTP 관련 에러 (연결, 타임아웃 등)은 pass
    except (httpx.RequestError, httpx.HTTPError, httpx.HTTPStatusError):
        return None

if __name__ == "__main__":
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)