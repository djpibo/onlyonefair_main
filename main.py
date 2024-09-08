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


@socketio.on('nfc_data', namespace='/')
def handle_nfc_data(response):
    print("[INFO] NFC 데이터 수신:", response)
    scr_dto: ScreenDTO = commander.start_card_polling(response['data'])
    if scr_dto is None:
        return
    tf = scr_dto.peer_name == "운영진"

    socketio.emit('polling_result', {
        'comment': scr_dto.comment,
        'acc_score': '대상 아님' if tf else int(scr_dto.acc_score),
        'current_score': '' if int(scr_dto.current_score) == 0 else f"(+{int(scr_dto.current_score)})",
        'photo': '무제한' if tf else int((scr_dto.acc_score - scr_dto.used_score) / 800),
        'peer_name': '운영진입니다' if tf else f"{scr_dto.peer_name}님",
        'peer_company': scr_dto.peer_company,
        'enter_dvcd': scr_dto.enter_dvcd_kor,
        'require_time': scr_dto.require_time,
    })


if __name__ == "__main__":
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
