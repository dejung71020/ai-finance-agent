# ai-finance-agent

```mermaid
graph TD
    %% 전체 프로젝트 루트
    Root[AI 자산 관리 에이전트: Personal Finance OS]

    %% 1. 데이터 통합 및 인프라 (Data Foundation)
    Root --> WP1[1. 데이터 통합 및 보안]
    WP1 --> F1_1[전 금융권 API 실시간 연동 - 은행/카드/증권/보험]
    WP1 --> F1_2[가상자산 거래소 및 지갑 통합]
    WP1 --> F1_3[포인트 및 마일리지 현금화 통합]
    WP1 --> F1_4[멀티 디바이스 동기화 - 워치/카/홈]
    WP1 --> F1_5[이상 거래 감지 시스템 - FDS]
    WP1 --> F1_6[사기 의심 계좌 실시간 탐지]
    WP1 --> F1_7[신용 점수 관리 및 가이드라인]

    %% 2. AI 분석 및 인터페이스 (AI Intelligence)
    Root --> WP2[2. AI 분석 및 인터페이스]
    WP2 --> F2_1[지출 99% 자동 분류 엔진]
    WP2 --> F2_2[대화형 LLM 인터페이스 - 자연어 질의응답]
    WP2 --> F2_3[뉴스 센티먼트 분석 및 포트폴리오 영향도]
    WP2 --> F2_4[재무 건강 진단 스코어링 시스템]
    WP2 --> F2_5[현금 흐름 시각화 - 샌키 플로우차트]
    WP2 --> F2_6[미래 잔고 예측 시뮬레이션 - 3~6개월]
    WP2 --> F2_7[인플레이션 반영 실질 자산 가치 측정]

    %% 3. 지출 관리 및 행동 경제학 (Spending & Psychology)
    Root --> WP3[3. 지출 관리 및 행동 가이드]
    WP3 --> F3_1[상황별 즉각적 소비 제안 - 커피 vs 여행]
    WP3 --> F3_2[예산 초과 임박 즉각 경고 및 중단 권고]
    WP3 --> F3_3[미래 가치 변환 알림 - 최신폰 vs 은퇴자금]
    WP3 --> F3_4[주간 동기부여 메시지 - 점심값 vs 주식]
    WP3 --> F3_5[택시비 기회비용 환산 - 잠을 사기 위한 비용]
    WP3 --> F3_6[무지출 챌린지 자동 기록 및 보너스 입금]
    WP3 --> F3_7[구독 서비스 미사용 감지 및 해지 권고]
    WP3 --> F3_8[유사 그룹 소비 패턴 비교 분석]

    %% 4. 투자 및 자산 최적화 (Investment & Optimization)
    Root --> WP4[4. 투자 및 자산 최적화]
    WP4 --> F4_1[로보어드바이저 - 글로벌 자산 배분 및 리밸런싱]
    WP4 --> F4_2[비상금 자동 예치 - 파킹통장 자동 이동]
    WP4 --> F4_3[저점 매수 타이밍 알림 - 증시 과매도 감지]
    WP4 --> F4_4[배당금 통합 관리 캘린더]
    WP4 --> F4_5[투자 오답 노트 - 매도 사유 기록 및 패턴 경고]
    WP4 --> F4_6[카드 실적 계산기 및 최적 혜택 안내]

    %% 5. 자금 흐름 자동화 (Workflow Automation)
    Root --> WP5[5. 자금 흐름 자동화]
    WP5 --> F5_1[자동 이체 최적화 - 잔고 맞춤 일정 조정]
    WP5 --> F5_2[월급날 자동 쪼개기 - 생활비/저축/비상금/투자]
    WP5 --> F5_3[목표 기반 저축 서비스 - 잔돈 모으기/정액]
    WP5 --> F5_4[고정비 자동 계산 및 납부 관리]
    WP5 --> F5_5[최적 적금 예산 자동 산정]

    %% 6. 세무 및 생애 주기 (Tax & Life Planning)
    Root --> WP6[6. 세무 및 생애 주기]
    WP6 --> F6_1[절세 계좌 최적화 - ISA/IRP 납입 한도 관리]
    WP6 --> F6_2[연말정산 실시간 시뮬레이터 - 카드 비중 교정]
    WP6 --> F6_3[해외 주식 양도소득세 절세 가이드]
    WP6 --> F6_4[중소기업 취업자 소득세 감면 추적]
    WP6 --> F6_5[생애 주기별 시나리오 점검 - 결혼/출산/은퇴]
    WP6 --> F6_6[경조사비 기록 및 가이드라인]
    WP6 --> F6_7[개인 자산 로드맵 퀘스트 및 뱃지 시스템]
    WP6 --> F6_8[할부 누적 시각화 및 통합 경고]
```

```mermaid
graph TD
    Root[<b>AI 자산 관리 에이전트</b>] -- "관제" --> WP1
    Root -- "지능" --> WP2
    Root -- "코칭" --> WP3
    Root -- "최적화" --> WP4
    Root -- "자동화" --> WP5
    Root -- "플랜" --> WP6

    subgraph WP1 [1. 데이터 및 보안]
        direction TB
        F1_1[금융 API 실시간 연동]
        F1_2[가상자산/지갑 통합]
        F1_3[포인트 현금화 통합]
        F1_4[멀티 디바이스 동기화]
        F1_5[이상 거래 감지 FDS]
        F1_6[사기 의심 계좌 탐지]
        F1_7[신용 점수 가이드]
    end

    subgraph WP2 [2. AI 분석/인터페이스]
        direction TB
        F2_1[지출 99% 분류 엔진]
        F2_2[대화형 LLM 인터페이스]
        F2_3[뉴스 센티먼트 분석]
        F2_4[재무 건강 스코어링]
        F2_5[현금 흐름 시각화]
        F2_6[미래 잔고 예측]
        F2_7[실질 자산 가치 측정]
    end

    subgraph WP3 [3. 지출/행동 가이드]
        direction TB
        F3_1[상황별 소비 제안]
        F3_2[예산 초과 경고]
        F3_3[미래 가치 변환 알림]
        F3_4[주간 동기부여 메시지]
        F3_5[택시비 기회비용 보고]
        F3_6[무지출 챌린지 기록]
        F3_7[구독 미사용 해지 권고]
        F3_8[유사 그룹 비교 분석]
    end

    subgraph WP4 [4. 투자 최적화]
        direction TB
        F4_1[로보어드바이저/리밸런싱]
        F4_2[비상금 파킹 자동 예치]
        F4_3[저점 매수 타이밍 알림]
        F4_4[배당금 통합 캘린더]
        F4_5[투자 오답 노트]
        F4_6[카드 실적 계산기]
    end

    subgraph WP5 [5. 자금 자동화]
        direction TB
        F5_1[자동 이체 일정 조정]
        F5_2[월급날 자동 쪼개기]
        F5_3[목표 기반 저축 퀘스트]
        F5_4[고정비 자동 납부 관리]
        F5_5[최적 적금 예산 산정]
    end

    subgraph WP6 [6. 세무 및 생애 주기]
        direction TB
        F6_1[절세 계좌 한도 관리]
        F6_2[연말정산 시뮬레이터]
        F6_3[해외주식 양도세 가이드]
        F6_4[소득세 감면 추적]
        F6_5[생애 주기 시나리오]
        F6_6[경조사비 가이드라인]
        F6_7[자산 로드맵 퀘스트]
        F6_8[할부 누적 통합 경고]
    end

    %% 스타일링
    style Root fill:#f9f,stroke:#333,stroke-width:4px
    style WP1 fill:#e1f5fe,stroke:#01579b
    style WP2 fill:#fff3e0,stroke:#e65100
    style WP3 fill:#f1f8e9,stroke:#33691e
```

```mindmap
mindmap
  root((AI 자산 관리 OS))
    데이터/보안
      금융 API 연동
      가상자산 통합
      포인트 현금화
      멀티 디바이스
      FDS/사기탐지
      신용점수 관리
    AI 지능
      99% 지출분류
      LLM 대화형 UI
      뉴스 센티먼트
      재무 건강진단
      현금흐름 시각화
      미래잔고 예측
      인플레 반영
    행동 코칭
      소비 제안/경고
      미래가치 변환
      동기부여 알림
      택시비 환산
      무지출 챌린지
      구독 해지 권고
      유사 그룹 비교
    투자/최적화
      로보어드바이저
      비상금 자동예치
      저점매수 타이밍
      배당 캘린더
      투자 오답노트
      카드 실적 계산
    자동화
      자동이체 최적화
      월급 통장쪼개기
      목표기반 저축
      고정비 관리
    세무/플랜
      절세계좌 관리
      연말정산 시뮬
      양도세 가이드
      소득세 감면추적
      생애주기 점검
      경조사비 가이드
      자산 로드맵
      할부 누적 경고
```

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
```
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
