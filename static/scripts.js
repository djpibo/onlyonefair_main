// Socket.IO 클라이언트 연결
const socket = io();

// 서버로부터 'nfc_data' 이벤트를 수신했을 때 실행되는 함수
socket.on('nfc_data', function(data) {
    document.getElementById('nfc-data').innerText = `NFC 데이터: ${data.data}`;
});

// 서버로부터 'polling_result' 이벤트를 수신했을 때 실행되는 함수
socket.on('polling_result', function(data) {
    // 각 변수 값을 HTML 요소에 표시
    document.getElementById('comment').innerText = data.comment;
    document.getElementById('title').innerText = `${data.peer_company}\n ${data.peer_name}님, ${data.enter_dvcd}`;
    document.getElementById('photo').innerText = `사용가능한 촬영권 \n\n ${data.photo}`;
    document.getElementById('acc_score').innerText = `현재까지 받은 포인트\n\n ${data.acc_score} (+${data.current_score})`;


    // polling-result 블록을 표시
    document.getElementById('polling-result').style.display = 'block';// 제목 변경
    document.getElementById('page-title').innerText = 'Polling 결과';


});

function padTime(unit) {
    return String(unit).padStart(2, '0');
}

function updateClock() {
    const now = new Date();

    // 현재 시각 표시
    const hours = padTime(now.getHours());
    const minutes = padTime(now.getMinutes());
    const seconds = padTime(now.getSeconds());
    const formattedTime = `${hours}:${minutes}:${seconds}`;
    document.getElementById('clock').innerText = formattedTime;

    // 현재 시각과 futureTime의 차이를 계산
    const timeDifference = futureTime - now;
    const diffHours = padTime(Math.floor((timeDifference / (1000 * 60 * 60)) % 24));
    const diffMinutes = padTime(Math.floor((timeDifference / (1000 * 60)) % 60));
    const diffSeconds = padTime(Math.floor((timeDifference / 1000) % 60));
    const formattedDifference = `${diffHours}:${diffMinutes}:${diffSeconds}`;
    document.getElementById('time-difference').innerText = `남은 시간: ${formattedDifference}`;
}

// 페이지 로드 시 시계 초기화
const now = new Date();
const futureTime = new Date(now.getTime() + 8 * 60 * 1000);

// futureTime을 표시
document.getElementById('future-time').innerText = `포인트를 획득 가능한 최소 퇴장 시간: ${padTime(futureTime.getHours())}:${padTime(futureTime.getMinutes())}:${padTime(futureTime.getSeconds())}`;

// 시계를 매초 업데이트
setInterval(updateClock, 1000);
updateClock();
