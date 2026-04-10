# Dockerfile

# python:3.11-slim 이미지 기반
FROM python:3.11-slim

# 컨테이너 내부 작업 디렉토리 -> /app
WORKDIR /app

# 컨테이너로 복사
COPY requirements.txt .

# 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 모든 파일 복사
COPY . .

# 컨테이너 포트 8000 노출
EXPOSE 8000

# 컨테이너 실행 시 FastAPI 서버 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]