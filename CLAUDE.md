# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 협업 방식

> **코드를 직접 타이핑하며 이해하고 싶다.**
> Claude는 코드를 직접 파일에 작성하지 말고, 다음 순서로 안내한다:
> 1. **작업 순서** — 어떤 파일을 어떤 순서로 작성할지 설명
> 2. **코드 제시** — 타이핑할 전체 코드를 코드 블록으로 제공
> 3. **설명** — 각 코드가 왜 필요한지 이유 설명
>
> 파일 자동 수정(Edit/Write 도구)은 사용하지 않는다.
>
> **단, CLAUDE.md 업데이트가 필요한 경우는 예외:**
> 1. 수정이 필요한 항목 목록을 번호와 함께 제시한다
> 2. 사용자에게 번호를 입력받는다
> 3. 선택된 항목만 직접 수정(Edit 도구)한다

## 프로젝트 개요

**AI 금융 비서 (Finance OS)** — 개인의 전 금융권 데이터를 통합하고 AI 에이전트가 행동 경제학 관점에서 지출을 코칭하며 자금 흐름을 자동화하는 대규모 개인 금융 OS.

10주 로드맵 / 8개 Phase / 모바일 앱 + n8n 자동화 + Docker 배포 포함. **Python 3.11.9** 사용. WBS 전체 내용은 `docs/AI_금융비서_WBS.docx.md` 참고.

## 실행 명령어

```bash
# 가상환경 활성화 (Windows)
venv\Scripts\activate

# FastAPI 서버 실행
uvicorn app.main:app --reload

# 테스트 실행
pytest tests/ -v

# 테스트 단일 파일 실행
pytest tests/test_users.py -v

# n8n 실행/종료 (Docker)
docker compose up -d
docker compose down

# 새 도메인 스캐폴딩
python scripts/generate_finance_domain.py
```

- API 문서: `http://localhost:8000/docs`
- n8n 대시보드: `http://localhost:5678`
- 헬스체크: `http://localhost:8000/health`

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
    config.py          # pydantic-settings + lru_cache 싱글턴, .env 자동 로드
    database.py        # SQLAlchemy engine/SessionLocal/Base, get_db
    lifespan.py        # 서버 시작: DB 테이블 생성 + Redis 연결 / 종료: 양쪽 해제
    cache.py           # RedisClient — connect/disconnect/get/set/delete
    event_bus.py       # EventBus — Redis Streams XADD 발행, 8개 스트림 초기화
    events/
      schemas.py       # EventEnvelope Pydantic 모델
    auth.py            # JWT 액세스(30분)/리프레시(7일) 토큰, get_current_user Depends
    encryption.py      # [예정 0.3.3] AES-256 암호화
  api/
    router.py          # 모든 도메인 라우터를 prefix="/api"로 통합 (ROUTERS START/END 마커)
  domains/
    {domain}/
      models.py        # SQLAlchemy 모델 (UUID PK, 단수 클래스명)
      schemas.py       # Pydantic V2 (Base / Create / Read)
      repository.py    # DB 접근 전용
      services.py      # 비즈니스 로직 + AI 에이전트 결합 지점
      router.py        # APIRouter prefix='/{domain}'
  main.py              # FastAPI 인스턴스, /, /health, app.include_router(router)
```

### 요청 흐름

```
클라이언트 → main.py → api/router.py → domains/{domain}/router.py
           → services.py → repository.py → models.py
                        └→ event_bus.publish()  [비동기 이벤트]
```

### 핵심 동작

- **DB 세션**: `get_db()`는 예외 발생 시 자동 `rollback()` 후 `close()`
- **Redis**: `get()`은 JSON 자동 역직렬화, `set()`은 dict/list를 JSON으로 자동 직렬화, 기본 TTL 3600초
- **커넥션 풀**: `pool_size=10`, `max_overflow=20`, `pool_recycle=3600`, `pool_pre_ping=True`
- **lifespan**: 서버 시작 시 `Base.metadata.create_all()` + Redis PING, 종료 시 양쪽 해제

### 이벤트 기반 구조 (0.2.3 설계 확정)

이벤트 스트리밍은 **Redis Streams** (Phase 0~4) → **Upstash Kafka** (Phase 7) 전략.
스트림 네이밍: `finance:{domain}` (e.g. `finance:transactions`)
이벤트 명명 규칙: `{도메인}.{엔티티}.{과거형동사}` (e.g. `transactions.transaction.created`)
상세 설계: `docs/0.2.3_event_driven_architecture.md`

### 핵심 규칙

- 도메인 라우터는 반드시 `app/api/router.py`에만 등록 (`main.py`에 직접 추가 금지)
- DB 세션은 모든 라우터에서 `Depends(get_db)` 사용
- Redis는 `from app.core.cache import redis_client` — lifespan이 자동 관리
- `settings`는 `from app.core.config import settings`로 어디서든 import
- 도메인 모델 클래스명은 **단수** 사용 (`User`, `Asset`, `Transaction`, `Investment`, `CoachSession`, `AutomationRule`, `PlanningGoal`)
- 이벤트 발행은 반드시 **DB 커밋 성공 후**에 실행 (미커밋 데이터 이벤트 금지)
- 보호된 엔드포인트는 `Depends(get_current_user)` 사용 (`from app.core.auth import get_current_user`)
- 이벤트 발행: `await event_bus.publish(stream, EventEnvelope(...))` — DB 커밋 후 호출

## 도메인별 컬럼 정의 시점

각 도메인의 실제 컬럼은 해당 기능 Phase에서 추가한다. 현재 `users` 만 완성 상태.

| 도메인 | 컬럼 완성 Phase | WBS ID |
|--------|----------------|--------|
| `users` | ✅ 완성 | — |
| `assets` | Phase 1 (3주차) | 1.4.1 |
| `transactions` | Phase 1 (3주차) | 1.4.2 |
| `investment` | Phase 1 (4주차) | 1.2.2 |
| `automation` | Phase 2 (6주차) | 2.3.x |
| `coach` | Phase 5 (8주차) | 5.x.x |
| `planning` | Phase 6 (9주차) | 6.3.x |

## 새 도메인 추가

1. `python scripts/generate_finance_domain.py` 실행
2. `models.py`에 컬럼 추가
3. `app/api/router.py`의 `ROUTERS START/END` 사이에 `router.include_router(...)` 추가

> ⚠️ 스캐폴드 스크립트의 `update_main_router()`는 `main.py`에 라우터를 등록하려 하지만, 이 프로젝트는 `app/api/router.py`에서 관리한다. 스크립트 실행 후 `main.py`에 생긴 import/include는 삭제하고 `api/router.py`에 수동 추가할 것.

## 환경 변수 (.env)

| 변수 | 필수 | 설명 |
|------|------|------|
| `POSTGRESQL_URL` | ✅ | Supabase PostgreSQL 연결 주소 |
| `REDIS_URL` | ✅ | Upstash Redis 연결 주소 |
| `SECRET_KEY` | ✅ | JWT 서명 키 |
| `DEBUG` | - | `True` 시 SQL 쿼리 로그 출력 + DEBUG 레벨 로깅 |
| `GOOGLE_API_KEY` | - | |
| `OPENAI_API_KEY` | - | |
| `ANTHROPIC_API_KEY` | - | |
| `XAI_API_KEY` | - | |

JWT 알고리즘은 `settings.ALGORITHM = "HS256"` (config.py 하드코딩).
인증 라이브러리: `python-jose[cryptography]`, `passlib[bcrypt]` (이미 requirements.txt에 포함).

GitHub Actions Secrets에도 동일하게 등록 필요 (`POSTGRESQL_URL`, `REDIS_URL`, `SECRET_KEY`, `RAILWAY_TOKEN`).

## CI/CD

- **CI** (`ci.yml`): PR → main 브랜치 시 `python -c "from app.main import app"` 임포트 검사 + `pytest tests/ -v` (tests 폴더 없으면 스킵)
- **Deploy** (`deploy.yml`): 현재 `workflow_dispatch` (수동 실행) — Phase 7 배포 환경 구성 시 자동화 예정

## 진행 현황

### Phase 0 완료 ✅
- ✅ 0.1.1 개발 환경 구성
- ✅ 0.1.2 PostgreSQL/Supabase 연결
- ✅ 0.1.3 Redis 세팅 (Upstash)
- ✅ 0.1.4 Docker Compose 구성 (n8n + Dockerfile)
- ✅ 0.1.5 GitHub Actions CI/CD
- ✅ 0.2.1 Layered Architecture 설계 (도메인 구조 확정)
- ✅ 0.2.2 도메인 스캐폴딩 완성 (7개 도메인 폴더 생성, users 컬럼 완성)
- ✅ 0.2.3 이벤트 기반 구조 설계 + 구현 → `docs/0.2.3_event_driven_architecture.md`, `app/core/event_bus.py`
- ✅ 0.3.1 JWT 인증 → `app/core/auth.py`, `docs/0.3.1.md`

### Phase 0 진행 중 🔄
- ⬜ 0.3.2 OAuth 연동 (카카오/네이버) — 외부 API 키 필요, 후순위
- ⬜ 0.3.3 AES-256 암호화 → `app/core/encryption.py`
