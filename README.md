### 📂 프로젝트 루트 구성 (최종)

이 구조는 도메인 기반 설계(Domain-Driven Design)를 채택하여, 기능이 늘어나도 코드가 꼬이지 않도록 설계되었습니다.

```text
ai-finance-agent/
├── app/
│   ├── core/              # DB 설정, 환경 변수, 보안 정책
│   ├── domains/           # 6개 WP별 도메인 로직 (핵심)
│   │   ├── users/         # 사용자 및 프로필
│   │   ├── assets/        # 금융/가상자산/포인트 연동
│   │   ├── transactions/  # AI 분류 및 거래 내역
│   │   ├── coach/         # 지출 가이드 및 심리 코칭
│   │   ├── investment/    # 로보어드바이저 및 리밸런싱
│   │   ├── automation/    # 자동 이체 및 워크플로우
│   │   └── planning/      # 세무 및 생애 주기 플랜
│   ├── utils/             # 공통 계산기 (인플레, 복리 등)
│   └── main.py            # API 엔드포인트 통합 및 실행
├── scripts/
│   └── generate_finance_domain.py  # 도메인 자동 생성 스크립트
├── .env.example           # 환경 변수 샘플
├── .gitignore             # Git 제외 목록
├── docker-compose.yml     # 로컬 DB 테스트용
├── requirements.txt       # 의존성 패키지
└── README.md              # 프로젝트 설명서
```

---

### 📝 최종 README.md 내용

아래 내용을 복사하여 `README.md`에 붙여넣으세요. 모든 기능 명세와 실행 방법이 포함되어 있습니다.

````markdown
# 🚀 AI 자산 관리 에이전트: Personal Finance OS

개인의 모든 금융 자산을 실시간으로 추적하고, AI 에이전트(버핏, 멍거 등)가 행동 경제학 관점에서 지출을 코칭하며, 복잡한 자금 흐름을 자동화하는 **차세대 개인 금융 관리 시스템**입니다.

---

## 🛠 Tech Stack

- **Framework:** FastAPI (Asynchronous Python)
- **Database:** Supabase (PostgreSQL + pgvector + TimescaleDB)
- **ORM:** SQLAlchemy (Layered Architecture)
- **AI Engine:** Gemini 1.5 Pro / GPT-4o (RAG 기반 상담)
- **Analysis:** pgvector (유사도 검색), Pandas (통계 분석)

---

## 🚀 Quick Start (실행 방법)

### 1. 가상 환경 및 패키지 설치

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
````

### 2\. 환경 변수 설정

`.env` 파일을 생성하고 Supabase 접속 정보를 입력합니다. (비밀번호 특수문자 주의)

```env
DATABASE_URL=postgresql://postgres:[PASSWORD]@[HOST]:5432/postgres
GEMINI_API_KEY=your_key_here
```

### 3\. Supabase 초기화 (SQL Editor에서 실행)

AI 분류 및 보안 기능을 위해 아래 명령어를 Supabase SQL Editor에서 실행하세요.

```sql
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

### 4\. 도메인 레이어 자동 생성

이슈 기반 개발을 위해 도메인 구조를 먼저 생성합니다.

```bash
python scripts/generate_finance_domain.py
# 입력창에 다음을 입력: users, assets, transactions, coach, investment, automation, planning
```

### 5\. 서버 실행

```bash
uvicorn app.main:app --reload
```

- **API 명세서:** [http://localhost:8000/docs](https://www.google.com/search?q=http://localhost:8000/docs)

---

## 📝 기능 명세 (Work Packages)

### WP 1. 데이터 통합 및 보안 (The Foundation)

- 전 금융권(은행/카드/보험/증권) 실시간 데이터 동기화
- 가상자산 거래소 및 개인 지갑(Web3) 통합 관리
- 이상 거래 감지(FDS) 및 사기 의심 계좌 실시간 필터링

### WP 2. AI 지능화 및 분석 (The Intelligence)

- **AI 분류:** 가맹점명 임베딩 기반 지출 99% 자동 분류
- **미래 예측:** 3\~6개월 후 잔고 시뮬레이션 및 인플레 반영 실질 가치 측정
- **대화형 UI:** RAG 기반 개인화 금융 상담 에이전트

### WP 3. 지출 및 행동 코칭 (The Coach)

- 상황별 소비 제안: "지금 커피 대신 그 돈으로 여행 자금을 만드세요"
- **미래 가치 변환:** 소비 금액을 10년 후 은퇴 자금 가치로 환산 시각화
  - 공식: $$FV = PV \times (1 + r)^n$$
- 구독 서비스 미사용 감지 및 해지 권고 자동화

### WP 4. 투자 및 자산 최적화 (The Optimization)

- 글로벌 자산 배분 로보어드바이저 및 리밸런싱 알림
- 뉴스 센티먼트 분석 기반 저점 매수 타이밍 포착
- 카드 실적 자동 계산 및 결제 수단 최적화 가이드

### WP 5. 자금 흐름 자동화 (The Workflow)

- 월급날 자동 쪼개기 시스템 (생활비/저축/투자)
- 잔고 상황에 맞춘 자동 이체 일정 최적화 및 비상금 예치

### WP 6. 세무 및 생애 주기 (The Roadmap)

- 연말정산 실시간 시뮬레이터 및 절세 계좌(ISA/IRP) 한도 관리
- 생애 주기 시나리오 점검 (결혼, 출산, 은퇴 대비 현금 흐름 분석)
- 할부 누적 시각화 및 통합 채무 경고 시스템

---

## 🤝 Contribution Guide

1.  모든 기능 구현은 `app/domains/` 내부의 레이어드 구조를 준수합니다.
2.  비즈니스 로직은 `services.py`에, DB 접근은 `repository.py`에 작성합니다.
3.  새로운 금융 수식 추가 시 `app/utils/`에 공통 함수로 등록합니다.

<!-- end list -->

```

---
```
