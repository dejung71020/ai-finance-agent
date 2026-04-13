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
    database.py        # SQLAlchemy engine/SessionLocal/Base(DeclarativeBase 2.0), get_db
    lifespan.py        # 서버 시작: DB 테이블 생성 + Redis 연결 / 종료: 양쪽 해제
    cache.py           # RedisClient — connect/disconnect/get/set/delete
    event_bus.py       # EventBus — Redis Streams XADD 발행, 8개 스트림 초기화
    events/
      schemas.py       # EventEnvelope Pydantic 모델
    auth.py            # JWT 액세스(30분)/리프레시(7일) 토큰, get_current_user Depends
    encryption.py      # AES-256-GCM 암호화/복호화 (encrypt/decrypt)
    ai_client.py       # GeminiClient 싱글턴 — gemini-2.5-flash-lite, generate(prompt) async
  api/
    router.py          # 모든 도메인 라우터를 prefix="/api"로 통합 (ROUTERS START/END 마커)
  domains/
    {domain}/
      models.py        # SQLAlchemy 모델 (UUID PK, 단수 클래스명)
      schemas.py       # Pydantic V2 (Base / Create / Read)
      repository.py    # DB 접근 전용
      services.py      # 비즈니스 로직 + AI 에이전트 결합 지점
      router.py        # APIRouter prefix='/{domain}'
      category_classifier.py  # (transaction 전용) Gemini 기반 카테고리 자동 분류
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
- **lifespan**: 서버 시작 시 `DEBUG=True`면 `drop_all()` 후 `create_all()` (스키마 초기화), `DEBUG=False`면 `create_all()`만 실행. Redis PING 후 이벤트 스트림 초기화. 종료 시 양쪽 해제

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
- 도메인 폴더명은 **단수** 사용 (`asset/`, `transaction/`, `investment/` 등) — URL prefix만 복수 (`/assets`, `/transactions`)
- 도메인 모델 클래스명은 **단수** 사용 (`User`, `Asset`, `Transaction`, `Investment`, `CoachSession`, `AutomationRule`, `PlanningGoal`)
- Service/Repository/Schema 클래스명도 **단수** 사용 (`AssetService`, `TransactionRepository`, `AssetCreate` 등)
- 이벤트 발행은 반드시 **DB 커밋 성공 후**에 실행 (미커밋 데이터 이벤트 금지)
- 보호된 엔드포인트는 `Depends(get_current_user)` 사용 (`from app.core.auth import get_current_user`)
- 이벤트 발행: `await event_bus.publish(stream, EventEnvelope(...))` — DB 커밋 후 호출
- Gemini AI 호출: `from app.core.ai_client import gemini_client` → `await gemini_client.generate(prompt)` — 도메인별 classifier에서만 사용

## 도메인별 컬럼 정의 시점

각 도메인의 실제 컬럼은 해당 기능 Phase에서 추가한다. 현재 `users`, `asset`, `transaction` 완성 상태.

| 도메인 | 컬럼 완성 Phase | WBS ID |
|--------|----------------|--------|
| `users` | ✅ 완성 | — |
| `asset` | ✅ 완성 | 1.4.1 |
| `transaction` | ✅ 완성 | 1.4.2 |
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
| `REDIS_URL` | ✅ | Upstash Redis 연결 주소 (**`rediss://`** TLS 필수, `redis://` 아님) |
| `SECRET_KEY` | ✅ | JWT 서명 키 |
| `ENCRYPTION_KEY` | ✅ | AES-256 암호화 키 (64자 hex, `python -c "import os; print(os.urandom(32).hex())"` 로 생성) |
| `DEBUG` | - | `True` 시 SQL 쿼리 로그 출력 + 서버 시작 시 테이블 전체 초기화 |
| `GEMINI_API_KEY` | - | Google AI Studio 발급 — `gemini-2.5-flash-lite` 모델 사용, `google-generativeai==0.8.3` 필요 |
| `OPENAI_API_KEY` | - | |
| `ANTHROPIC_API_KEY` | - | |
| `XAI_API_KEY` | - | |

JWT 알고리즘은 `settings.ALGORITHM = "HS256"` (config.py 하드코딩).
인증 라이브러리: `python-jose[cryptography]`, `passlib[bcrypt]` (이미 requirements.txt에 포함).
`bcrypt==4.0.1` 버전 고정 필수 — `passlib 1.7.4`는 `bcrypt 4.1+`와 호환되지 않음.

GitHub Actions Secrets에도 동일하게 등록 필요 (`POSTGRESQL_URL`, `REDIS_URL`, `SECRET_KEY`, `ENCRYPTION_KEY`, `RAILWAY_TOKEN`).

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
- ✅ 0.3.1 JWT 인증 → `app/core/auth.py`
- ✅ 0.3.3 AES-256-GCM 암호화 → `app/core/encryption.py`

### Phase 0 보류 ⏸
- ⬜ 0.3.2 OAuth 연동 (카카오/네이버) — 외부 API 키 필요, 후순위

### Phase 1 진행 중 🔄
- ✅ 1.4.1 Assets 테이블 설계/구현 → `app/domains/asset/`
- ✅ 1.4.2 Transactions 테이블 설계/구현 → `app/domains/transaction/`

### Phase 3 진행 중 🔄
- ✅ 3.1.1 거래 카테고리 자동 분류 (LLM) → `app/domains/transaction/category_classifier.py`

## 전체 태스크 구현 순서

| 순서 | Phase | ID | 작업 | 상태 |
|------|-------|----|------|------|
| 1 | 0 | 0.1.1 | 개발 환경 구성 | ✅ |
| 2 | 0 | 0.1.2 | PostgreSQL/Supabase 연결 | ✅ |
| 3 | 0 | 0.1.3 | Redis 세팅 | ✅ |
| 4 | 0 | 0.1.4 | Docker Compose 구성 | ✅ |
| 5 | 0 | 0.1.5 | GitHub Actions CI/CD | ✅ |
| 6 | 0 | 0.2.1 | Layered Architecture 설계 | ✅ |
| 7 | 0 | 0.2.2 | 도메인 스캐폴딩 | ✅ |
| 8 | 0 | 0.2.3 | 이벤트 기반 구조 설계 | ✅ |
| 9 | 0 | 0.3.1 | JWT 인증 구현 | ✅ |
| 10 | 0 | 0.3.3 | AES-256-GCM 암호화 | ✅ |
| 11 | 0 | 0.3.2 | OAuth 연동 (카카오/네이버) | ⏸ |
| 12 | 1 | 1.4.1 | Assets 테이블 설계/구현 | ✅ |
| 13 | 1 | 1.4.2 | Transactions 테이블 설계/구현 | ✅ |
| 14 | 3 | 3.1.1 | 거래 카테고리 자동 분류 (LLM) | ✅ |
| 15 | 1 | 1.3.3 | 거래 내역 정규화 | ⬜ |
| 16 | 1 | 1.3.1 | 데이터 동기화 스케줄러 | ⬜ |
| 17 | 1 | 1.3.2 | Webhook 수신 엔드포인트 | ⬜ |
| 18 | 1 | 1.5.1 | FDS 이상거래 감지 | ⬜ |
| 19 | 1 | 1.5.2 | 사기 의심 계좌 탐지 | ⬜ |
| 20 | 1 | 1.2.4 | 업비트 가상자산 API 연동 | ⬜ |
| 21 | 1 | 1.2.1 | 오픈뱅킹 API 연동 | ⬜ |
| 22 | 1 | 1.2.2 | 증권 API 연동 | ⬜ |
| 23 | 1 | 1.2.3 | 카드사 API 연동 | ⬜ |
| 24 | 1 | 1.2.5 | 포인트/마일리지 수집 | ⬜ |
| 25 | 1 | 1.1.1 | 모바일 앱 프레임워크 선택/세팅 | ⬜ |
| 26 | 1 | 1.1.2 | 로그인/회원가입 UI | ⬜ |
| 27 | 1 | 1.1.3 | 계좌 연결 UI | ⬜ |
| 28 | 1 | 1.6.1 | 멀티 디바이스 동기화 설계 | ⬜ |
| 29 | 3 | 3.1.2 | 고정비 자동 탐지 | ⬜ |
| 30 | 3 | 3.1.4 | 이상치 탐지 모델 | ⬜ |
| 31 | 3 | 3.2.1 | 현금흐름 시각화 API | ⬜ |
| 32 | 3 | 3.4.1 | 챗봇 API (자연어 질의) | ⬜ |
| 33 | 3 | 3.2.2 | 미래 잔고 예측 모델 | ⬜ |
| 34 | 3 | 3.5.1 | 포트폴리오 분석 엔진 | ⬜ |
| 35 | 3 | 3.5.2 | 리밸런싱 알고리즘 | ⬜ |
| 36 | 3 | 3.1.3 | 소비 패턴 군집화 | ⬜ |
| 37 | 3 | 3.2.3 | 인플레이션 반영 자산 계산 | ⬜ |
| 38 | 3 | 3.3.1 | 뉴스 감정 분석 | ⬜ |
| 39 | 2 | 2.1.2 | n8n ↔ FastAPI Webhook 연결 | ⬜ |
| 40 | 2 | 2.2.1 | 거래 발생 이벤트 트리거 | ⬜ |
| 41 | 2 | 2.2.2 | 잔액 변화 트리거 | ⬜ |
| 42 | 2 | 2.2.3 | 급격한 소비 증가 트리거 | ⬜ |
| 43 | 2 | 2.4.1 | 알림 채널 연동 (Slack/이메일) | ⬜ |
| 44 | 2 | 2.4.2 | 카카오톡/푸시 알림 연동 | ⬜ |
| 45 | 2 | 2.5.1 | n8n → FastAPI AI 에이전트 호출 | ⬜ |
| 46 | 2 | 2.3.1 | 자동 이체 워크플로우 | ⬜ |
| 47 | 2 | 2.3.2 | 비상금 파킹통장 자동 이동 | ⬜ |
| 48 | 2 | 2.3.3 | 저점 매수 자동화 트리거 | ⬜ |
| 49 | 4 | 4.1.1 | 룰 기반 자동 이체 엔진 | ⬜ |
| 50 | 4 | 4.2.1 | 실시간 지출 피드백 시스템 | ⬜ |
| 51 | 4 | 4.4.1 | 카드 실적 계산기 | ⬜ |
| 52 | 4 | 4.5.1 | 할부 누적 시각화 | ⬜ |
| 53 | 4 | 4.1.2 | AI 기반 이체 최적화 | ⬜ |
| 54 | 4 | 4.3.1 | ISA/IRP 최적화 엔진 | ⬜ |
| 55 | 4 | 4.3.2 | 연말정산 시뮬레이터 | ⬜ |
| 56 | 4 | 4.6.1 | 신용 점수 모니터링 | ⬜ |
| 57 | 5 | 5.2.1 | 예산 초과 즉각 경고 시스템 | ⬜ |
| 58 | 5 | 5.1.1 | 상황별 소비 제안 AI | ⬜ |
| 59 | 5 | 5.1.2 | 미래 가치 변환 엔진 | ⬜ |
| 60 | 5 | 5.3.1 | 동기부여 메시지 생성 AI | ⬜ |
| 61 | 5 | 5.1.3 | 기회비용 보고 | ⬜ |
| 62 | 5 | 5.2.2 | 구독 해지 권고 엔진 | ⬜ |
| 63 | 5 | 5.3.2 | 무지출 챌린지 시스템 | ⬜ |
| 64 | 6 | 6.1.1 | 재무 건강 스코어 엔진 | ⬜ |
| 65 | 6 | 6.3.1 | 목표 기반 저축 (Quest) | ⬜ |
| 66 | 6 | 6.1.2 | 월간 종합 리포트 생성 | ⬜ |
| 67 | 6 | 6.2.1 | 유사 그룹 비교 분석 | ⬜ |
| 68 | 6 | 6.3.2 | 자산 로드맵 게임화 | ⬜ |
| 69 | 6 | 6.4.1 | 생애 주기 시나리오 시뮬레이터 | ⬜ |
| 70 | 7 | 7.1.1 | 전체 Docker Compose 완성 | ⬜ |
| 71 | 7 | 7.1.2 | 환경변수 관리 체계 | ⬜ |
| 72 | 7 | 7.2.1 | AWS/GCP 배포 환경 구성 | ⬜ |
| 73 | 7 | 7.2.2 | HTTPS/도메인 설정 | ⬜ |
| 74 | 7 | 7.3.1 | 로그 모니터링 구축 | ⬜ |
| 75 | 7 | 7.5.1 | 실시간 이벤트 스트리밍 (Kafka) | ⬜ |
| 76 | 7 | 7.4.1 | Auto Scaling 설정 | ⬜ |
| 77 | 8 | 8.1.1 | 단위 테스트 (pytest) | ⬜ |
| 78 | 8 | 8.1.2 | 통합 테스트 | ⬜ |
| 79 | 8 | 8.1.3 | 금융 시나리오 테스트 | ⬜ |
| 80 | 8 | 8.1.4 | 보안 테스트 | ⬜ |
