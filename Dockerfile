# ── 베이스 이미지 ──────────────────────────────────────────
FROM python:3.11-slim

# ── 시스템 패키지 (FAISS CPU 빌드에 필요) ─────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# ── 작업 디렉터리 ──────────────────────────────────────────
WORKDIR /app

# ── 의존성 먼저 복사 (레이어 캐시 활용) ───────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── 소스 전체 복사 ─────────────────────────────────────────
# .dockerignore로 불필요한 파일 제외됨
COPY . .

# ── Streamlit 포트 ─────────────────────────────────────────
EXPOSE 8501

# ── 헬스체크 ──────────────────────────────────────────────
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# ── 실행 ──────────────────────────────────────────────────
ENTRYPOINT ["streamlit", "run", "app.py", \
    "--server.port=8501", \
    "--server.address=0.0.0.0", \
    "--server.headless=true"]
