from flask import Flask, render_template
from flask_socketio import SocketIO, emit

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
    company_name = "param1"
    nfc_data = "param2"
    return render_template('index.html', company=company_name, nfc_data=nfc_data)


@socketio.on('nfc_data')
def handle_nfc_data(response):
    print("NFC 데이터 수신:", response)
    # start_card_polling 함수가 5개의 변수를 반환한다고 가정
    # var1, var2, var3, var4, var5 = commander.start_card_polling(response['data'])
    scr_dto: ScreenDTO = commander.start_card_polling(response['data'])
    # 클라이언트에 반환된 결과를 전송
    socketio.emit('polling_result', {
        'comment': scr_dto.comment,
        'acc_score': int(scr_dto.acc_score),
        'current_score': int(scr_dto.current_score),
        'photo': int((scr_dto.acc_score - scr_dto.used_score)/800),
        'peer_name': scr_dto.peer_name,
        'peer_company': scr_dto.peer_company,
        'enter_dvcd': scr_dto.enter_dvcd_kor,
    })


if __name__ == "__main__":
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)