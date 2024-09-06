// Socket.IO 클라이언트 연결
const socket = io();

// 서버로부터 'nfc_data' 이벤트를 수신했을 때 실행되는 함수
socket.on('nfc_data', function(data) {
    document.getElementById('nfc-data').innerText = `NFC 데이터: ${data.data}`;
});

// 서버로부터 'polling_result' 이벤트를 수신했을 때 실행되는 함수
socket.on('polling_result', function(data) {

    console.log("polling- display")

    let accScoreText = `현재까지 받은 포인트\n\n ${data.acc_score}`;
    if (data.current_score !== 0) {
        accScoreText += ` (+${data.current_score})`;
    }
    document.getElementById('comment').innerText = data.comment;
    document.getElementById('title').innerText = `${data.peer_company}\n ${data.peer_name}님, ${data.enter_dvcd}`;
    document.getElementById('photo').innerText = `사용가능한 촬영권\n\n  ${data.photo}`;
    document.getElementById('acc_score').innerText = accScoreText;

    const now = new Date();
    const futureTime = new Date(now.getTime() + data.require_time * 60 * 1000);
    updateClock(futureTime);

    if (data.enter_dvcd == '입장') {
        document.getElementById('future-time').style.display = 'block';
        document.getElementById('future-time').innerText
        = `${padTime(futureTime.getHours())}:${padTime((futureTime.getMinutes() + 1) % 60)} 부터 포인트 획득 가능`;
    }
    else{
        document.getElementById('future-time').style.display = 'none';
    }
    setInterval(() => updateClock(futureTime), 1000);
});

function padTime(unit) {
    return String(unit).padStart(2, '0');
}

function updateClock(futureTime) {
    const now = new Date();

    // 현재 시각 표시
    const hours = padTime(now.getHours());
    const minutes = padTime(now.getMinutes());
    const seconds = padTime(now.getSeconds());
    const formattedTime = `${hours}:${minutes}:${seconds}`;
    document.getElementById('clock').innerText = formattedTime;

    // 현재 시각과 futureTime의 차이를 계산
//    let timeDifference = futureTime - now;
//
//    if (timeDifference <= 0) {
//        timeDifference = 0; // 0 이하일 경우 0으로 고정
//    }
//
//    const diffHours = padTime(Math.floor((timeDifference / (1000 * 60 * 60)) % 24));
//    const diffMinutes = padTime(Math.floor((timeDifference / (1000 * 60)) % 60));
//    const diffSeconds = padTime(Math.floor((timeDifference / 1000) % 60));
//    const formattedDifference = `${diffHours}:${diffMinutes}:${diffSeconds}`;
//    document.getElementById('time-difference').innerText = `남은 시간: ${formattedDifference}`;
}