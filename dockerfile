# Base image
FROM python:3.9-slim

# 시스템 패키지 및 빌드 도구 설치
RUN apt-get update && \
    apt-get install -y \
    libpcsclite1 \
    pcscd \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사
COPY requirements.txt .

# 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 소스 복사
COPY . .

# 컨테이너에서 실행할 명령어
CMD ["python", "main.py"]
