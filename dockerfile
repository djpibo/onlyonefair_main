# Base image 선택 (Python 버전에 따라 선택)
FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필요 패키지 복사 및 설치
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 파일 복사
COPY . .

# 실행할 명령어 설정 (예: Flask 앱 실행)
CMD ["python", "main.py"]
