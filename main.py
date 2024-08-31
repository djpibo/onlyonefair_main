from flask import Flask, render_template
from flask_socketio import SocketIO, emit

from injector import Injector
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

@socketio.on('nfc_data')
def handle_nfc_data(response):
    print("NFC 데이터 수신:", response)
    commander.start_card_polling(response['data'])
    emit('nfc_data', response, broadcast=True)

@socketio.on('company_enter')
def handle_nfc_data(data):
    print("회사, 입장구분코드:", data)
    emit('company_enter', data, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)