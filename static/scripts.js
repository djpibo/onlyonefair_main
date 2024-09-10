const socket = io();

socket.on('polling_result', function(data) {
    console.log("polling_result calls")
    localStorage.setItem('pollingData', JSON.stringify(data));
    window.location.href = "/index";
});

window.onload = function() {
    // localStorage에서 데이터 가져오기
    var data = JSON.parse(localStorage.getItem('pollingData'));

    // 데이터가 존재하면 화면 업데이트
    if (data) {
        document.getElementById('comment').innerText = data.comment;
        document.getElementById('title').innerText = `${data.peer_company}\n ${data.peer_name}, ${data.enter_dvcd}`;
        document.getElementById('photo').innerText = `사용가능한 촬영권\n\n  ${data.photo}`;
        document.getElementById('acc_score').innerText = `현재까지 받은 포인트\n\n ${data.acc_score}${data.current_score}`;

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

        localStorage.removeItem('pollingData');
    } else {
        console.log("No polling data found in localStorage");
    }

    let countdown = 3;
    const timerElement = document.getElementById('timer');
    const interval = setInterval(function() {
        timerElement.innerText = `${countdown}s lefts`;
        if (countdown === 0) {
            clearInterval(interval);
        }
        countdown--;
    }, 1000);
};

function showClock(data){
    if (data.enter_dvcd == '입장') {
        document.getElementById('future-time').style.display = 'block';
        document.getElementById('future-time').innerText
        = `${padTime(futureTime.getHours())}:${padTime((futureTime.getMinutes() + 1) % 60)} 부터 포인트 획득 가능`;
    }
    else{
        document.getElementById('future-time').style.display = 'none';
    }
    setInterval(() => updateClock(futureTime), 1000);
}

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
}