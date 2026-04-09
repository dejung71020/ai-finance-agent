# ai-finance-agent

## 프로젝트 개요

AI 자산 관리 에이전트: Personal Finance OS

`````mermaid
graph TD
    %% 전체 프로젝트 루트
    Root[AI 자산 관리 에이전트: Personal Finance OS]

    %% 워크패키지 연결
    Root --> WP1[1. 데이터 통합 및 보안]
    Root --> WP2[2. AI 분석 및 인터페이스]
    Root --> WP3[3. 지출 관리 및 행동 가이드]
    Root --> WP4[4. 투자 및 자산 최적화]
    Root --> WP5[5. 자금 흐름 자동화]
    Root --> WP6[6. 세무 및 생애 주기]

    %% 서브그래프
    subgraph WP1 ["1. 데이터 및 보안"]
        direction TB
        F1_1[금융 API 실시간 연동]
        F1_2[가상자산/지갑 통합]
        F1_3[포인트 현금화 통합]
        F1_4[멀티 디바이스 동기화]
        F1_5[이상 거래 감지 FDS]
        F1_6[사기 의심 계좌 탐지]
        F1_7[신용 점수 가이드]
    end

    subgraph WP2 ["2. AI 분석/인터페이스"]
        direction TB
        F2_1[지출 99% 자동 분류]
        F2_2[대화형 LLM 인터페이스]
        F2_3[뉴스 센티먼트 분석]
        F2_4[재무 건강 스코어링]
        F2_5[현금 흐름 시각화]
        F2_6[미래 잔고 예측]
        F2_7[인플레이션 반영 가치 측정]
    end

    subgraph WP3 ["3. 지출/행동 가이드"]
        direction TB
        F3_1[상황별 소비 제안]
        F3_2[예산 초과 경고]
        F3_3[미래 가치 변환 알림]
        F3_4[주간 동기부여 메시지]
        F3_5[택시비 기회비용 환산]
        F3_6[무지출 챌린지]
        F3_7[구독 미사용 해지 권고]
        F3_8[유사 그룹 소비 비교]
    end

    subgraph WP4 ["4. 투자 최적화"]
        direction TB
        F4_1[로보어드바이저 & 리밸런싱]
        F4_2[비상금 자동 예치]
        F4_3[저점 매수 타이밍 알림]
        F4_4[배당금 통합 캘린더]
        F4_5[투자 오답 노트]
        F4_6[카드 실적 계산기]
    end

    subgraph WP5 ["5. 자금 자동화"]
        direction TB
        F5_1[자동 이체 최적화]
        F5_2[월급날 자동 쪼개기]
        F5_3[목표 기반 저축]
        F5_4[고정비 자동 관리]
        F5_5[최적 적금 예산 산정]
    end

    subgraph WP6 ["6. 세무 및 생애 주기"]
        direction TB
        F6_1[절세 계좌 최적화]
        F6_2[연말정산 시뮬레이터]
        F6_3[해외주식 양도세 가이드]
        F6_4[소득세 감면 추적]
        F6_5[생애 주기 시나리오]
        F6_6[경조사비 가이드]
        F6_7[자산 로드맵 퀘스트]
        F6_8[할부 누적 경고]
    end

    %% 스타일링
    style Root fill:#f9f,stroke:#333,stroke-width:4px
    style WP1 fill:#e1f5fe,stroke:#01579b
    style WP2 fill:#fff3e0,stroke:#e65100
    style WP3 fill:#f1f8e9,stroke:#33691e

````markdown
📑 AI Finance Assistant (Backend)
사용자의 금융 데이터를 분석하여 지능적인 코칭과 자동화를 제공하는 AI 비서 서비스

본 프로젝트는 **FastAPI**와 **Supabase**(PostgreSQL + pgvector)를 기반으로 구축되었으며, 총 **45개의 핵심 금융 관리 기능**을 포함하고 있습니다.

### 🛠 Tech Stack

- **Framework**: FastAPI
- **Database**: Supabase (PostgreSQL + pgvector)
- **ORM**: SQLAlchemy
- **Language**: Python 3.10+
- **AI**: Gemini / OpenAI API (예정)

### Getting Started

#### 1. Prerequisites

- Python 3.10 이상 설치
- Supabase 프로젝트 생성 및 DB 암호 준비

#### 2. Environment Setup

먼저 프로젝트를 클론하고 가상 환경을 구축합니다.

```bash
# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 필수 패키지 설치
pip install -r requirements.txt
`````

````

#### 3. Database & Secret Configuration

루트 디렉토리에 `.env` 파일을 생성하고 Supabase 연결 정보를 입력합니다.

```env
# .env
DATABASE_URL=postgresql://postgres:[PASSWORD]@[HOST]:5432/postgres
OPENAI_API_KEY=your_api_key_here
GEMINI_API_KEY=your_api_key_here
```

**주의**: Supabase SQL Editor에서 다음 명령어를 반드시 실행해야 합니다.

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

#### 4. Domain Generation (Boilerplate)

기획된 도메인(users, assets, transactions 등)을 한 번에 생성합니다.

```bash
python generate_finance_domain.py
```

실행 후 입력창에 생성할 도메인을 콤마(,)로 구분하여 입력하세요.

**예시**: `users, assets, transactions, fixed_costs`

#### 5. Running the Server

로컬 개발 서버를 실행합니다.

```bash
uvicorn app.main:app --reload
```

서버가 정상적으로 시작되면 **http://localhost:8000/docs** 에서 Swagger UI를 통해 API 명세서를 확인할 수 있습니다.

### 📂 Project Structure

```plaintext
app/
├── core/                  # DB 설정 및 공통 보안 설정
├── domains/               # 기능별 도메인 (Layered Architecture)
│   └── [domain]/          # router, service, repository, models
├── main.py                # API 진입점 및 라우터 등록
└── utils/                 # 공통 유틸리티 함수
```

### 📝 Roadmap (Work Packages)

- **WP 1**: 전 금융권 데이터 통합 및 보안 인프라 구축
- **WP 2**: AI 지출 분류 및 현금 흐름 분석
- **WP 3**: 자동 이체 최적화 및 투자 리밸런싱
- **WP 4**: 상황별 소비 제안 및 미래 가치 환산
- **WP 5**: 재무 건강 진단 및 생애 주기 시나리오

### 🤝 Contributing

1. 이슈를 확인하고 브랜치를 생성합니다 (`feature/이슈번호-기능명`).
2. `generate_finance_domain.py`를 활용해 일관된 구조로 코드를 작성합니다.
3. PR을 생성하여 리뷰를 요청합니다.

```

```
````
