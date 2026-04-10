# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 개요

**AI 금융 비서 (Finance OS)** — 개인의 전 금융권 데이터를 통합하고 AI 에이전트가 행동 경제학 관점에서 지출을 코칭하며 자금 흐름을 자동화하는 대규모 개인 금융 OS.

10주 로드맵 / 8개 Phase / 모바일 앱 + n8n 자동화 + Docker 배포 포함. **Python 3.11.9** 사용. WBS 전체 내용은 `C:\KDT\개인포트폴리오\AI_금융비서_WBS.docx.md` 참고.

## 실행 명령어

```bash
# 가상환경 활성화 (Windows)
venv\Scripts\activate

# FastAPI 서버 실행
uvicorn app.main:app --reload

# n8n 실행/종료 (Docker)
docker compose up -d
docker compose down

# 새 도메인 스캐폴딩
python scripts/generate_finance_domain.py
```

- API 문서: `http://localhost:8000/docs`
- n8n 대시보드: `http://localhost:5678`

## 인프라 구성

| 서비스 | 방식 |
|--------|------|
| PostgreSQL | Supabase 클라우드 (`POSTGRESQL_URL`) |
| Redis | Upstash 클라우드 (`REDIS_URL`) |
| n8n | Docker (`docker-compose.yml`, 로컬 5678 포트) |
| FastAPI | 로컬 개발 / Railway 배포 (`Dockerfile` 준비됨) |

## 아키텍처

### 레이어 구조

```
app/
  core/
    config.py     # pydantic-settings + lru_cache 싱글턴, .env 자동 로드
    database.py   # SQLAlchemy engine/SessionLocal/Base, get_db
    lifespan.py   # 서버 시작: DB 테이블 생성 + Redis 연결 / 종료: 양쪽 해제
    cache.py      # RedisClient — connect/disconnect/get/set/delete
  api/
    router.py     # 모든 도메인 라우터를 prefix="/api"로 통합 (ROUTERS START/END 마커)
  domains/
    {domain}/
      models.py       # SQLAlchemy 모델 (UUID PK, pgvector 지원)
      schemas.py      # Pydantic V2 (Base / Create / Read)
      repository.py   # DB 접근 전용
      services.py     # 비즈니스 로직 + AI 에이전트 결합 지점
      router.py       # APIRouter prefix='/{domain}'
  main.py         # FastAPI 인스턴스, /health, app.include_router(router)
```

### 요청 흐름

```
클라이언트 → main.py → api/router.py → domains/{domain}/router.py
           → services.py → repository.py → models.py
```

### 핵심 규칙

- 도메인 라우터는 반드시 `app/api/router.py`에만 등록 (`main.py`에 직접 추가 금지)
- DB 세션은 모든 라우터에서 `Depends(get_db)` 사용
- Redis는 `from app.core.cache import redis_client` — lifespan이 자동 관리
- `settings`는 `from app.core.config import settings`로 어디서든 import

## 새 도메인 추가

1. `python scripts/generate_finance_domain.py` 실행
2. `models.py`에 컬럼 추가
3. `app/api/router.py`의 `ROUTERS START/END` 사이에 `router.include_router(...)` 추가

## 환경 변수 (.env)

| 변수 | 필수 |
|------|------|
| `POSTGRESQL_URL` | ✅ |
| `REDIS_URL` | ✅ |
| `SECRET_KEY` | ✅ |
| `GOOGLE_API_KEY` | - |
| `OPENAI_API_KEY` | - |
| `ANTHROPIC_API_KEY` | - |

GitHub Actions Secrets에도 동일하게 등록 필요 (`POSTGRESQL_URL`, `REDIS_URL`, `SECRET_KEY`, `RAILWAY_TOKEN`).

## Phase 0 진행 현황

- ✅ 0.1.1 개발 환경 구성
- ✅ 0.1.2 PostgreSQL/Supabase 연결
- ✅ 0.1.3 Redis 세팅 (Upstash)
- ✅ 0.1.4 Docker Compose 구성 (n8n + Dockerfile)
- ✅ 0.1.5 GitHub Actions CI/CD
- ⬜ 0.2.3 이벤트 기반 구조 설계 (Kafka/Redis Stream)
- ⬜ 0.3.1 JWT 인증 → `app/core/auth.py`
- ⬜ 0.3.2 OAuth 연동 (카카오/네이버)
- ⬜ 0.3.3 AES-256 암호화 → `app/core/encryption.py`
