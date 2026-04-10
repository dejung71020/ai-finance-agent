**AI 금융 비서 (Finance OS)**

**완전 구현 WBS (Work Breakdown Structure)**

WP1\~5 \+ 모바일 앱 \+ n8n 자동화 \+ Docker 배포 | 총 10주 로드맵

# **📦 기술 스택 (Tech Stack)**

| 카테고리 | 기술/도구 |
| :---: | ----- |
| **Backend** | Python 3.11, FastAPI, SQLAlchemy, Pydantic V2, Celery, APScheduler |
| **Database** | PostgreSQL (Supabase), pgvector, Redis (캐시/큐) |
| **AI/ML** | GPT-4o / GPT-4o-mini, LangChain, Prophet/LSTM, scikit-learn, BERT |
| **자동화** | n8n (Docker), Webhook, Kafka / Redis Stream |
| **Mobile** | React Native 또는 Flutter, FCM 푸시 알림 |
| **DevOps** | Docker, Docker Compose, GitHub Actions, AWS/GCP, Nginx, Grafana |
| **금융 API** | 금융결제원 오픈뱅킹, 토스증권, 업비트, KCB/NICE 신용, 카드사 API |
| **보안** | JWT, OAuth 2.0, AES-256 암호화, FDS, HTTPS/SSL |

# **🔗 Phase 간 의존 관계**

| 선행 Phase | 후행 Phase | 의존 이유 |
| :---: | :---: | ----- |
| **Phase 0** | **모든 Phase** | DB, 인프라, 인증 없이 구현 불가 |
| **Phase 1 (1.2-1.4)** | **Phase 3, 4, 5, 6** | 실제 금융 데이터 없이 AI 분석 불가 |
| **Phase 2 (n8n)** | **Phase 4 자동이체** | 자동화 워크플로우 기반 필요 |
| **Phase 3 (AI 분류)** | **Phase 5 코치** | 소비 분류 완성 후 행동 코칭 가능 |
| **Phase 1 (FDS)** | **Phase 4 (실시간 피드백)** | 이상 탐지 모델 선행 필요 |
| **Phase 3 (예측 모델)** | **Phase 4 (이체 최적화)** | 잔고 예측 기반 최적화 |

# **📋 WBS 전체 상세 (구현 순서 기준)**

**🧱 Phase 0\. 프로젝트 기반 세팅 (Foundation Layer)**

| ID | WP | 작업명 | 상세 내용 | 산출물 | 담당 | 주차 | 우선순위 | 상태 |
| :---: | :---: | ----- | ----- | ----- | :---: | :---: | :---: | :---: |
| **0.1.1** | 기반 | **개발 환경 구성** | Python 3.12, FastAPI, 가상환경(venv/pyenv) 세팅 | requirements.txt, .env.example | 전체 | 1 | 🔴 Critical | ⬜ 예정 |
| **0.1.2** | 기반 | **PostgreSQL / Supabase 연결** | DB 연결, SessionLocal, Base 설정 (database.py) | app/core/database.py | BE | 1 | 🔴 Critical | ⬜ 예정 |
| **0.1.3** | 기반 | **Redis 세팅** | 캐시 및 큐용 Redis 연결 설정, 세션/토큰 캐싱 구조 | app/core/cache.py | BE | 1 | 🟠 High | ⬜ 예정 |
| **0.1.4** | 기반 | **Docker Compose 구성** | FastAPI \+ PostgreSQL \+ Redis \+ n8n 컨테이너 정의 | docker-compose.yml | DevOps | 1 | 🔴 Critical | ⬜ 예정 |
| **0.1.5** | 기반 | **GitHub Actions CI/CD** | PR → 테스트 자동화, main 브랜치 배포 파이프라인 | .github/workflows/ | DevOps | 1 | 🟠 High | ⬜ 예정 |
| **0.2.1** | 기반 | **Layered Architecture 설계** | Controller/Service/Repository 레이어 분리, 도메인 구조 확정 | 아키텍처 문서, generate\_finance\_domain.py 실행 | 전체 | 1 | 🔴 Critical | ⬜ 예정 |
| **0.2.2** | 기반 | **도메인 스캐폴딩 실행** | users, assets, transactions, automation, investment, coach, planning 도메인 자동 생성 | app/domains/ 전체 구조 | BE | 1 | 🔴 Critical | ⬜ 예정 |
| **0.2.3** | 기반 | **이벤트 기반 구조 설계** | Pub/Sub 패턴, 도메인 이벤트 정의, Kafka/Redis Stream 선택 | 이벤트 설계 문서 | BE | 2 | 🟠 High | ⬜ 예정 |
| **0.3.1** | 기반 | **JWT 인증 구현** | 액세스/리프레시 토큰, 미들웨어 보안 설정 | app/core/auth.py | BE | 2 | 🔴 Critical | ⬜ 예정 |
| **0.3.2** | 기반 | **OAuth 연동** | 카카오/네이버 소셜 로그인, 금융 API 인증 흐름 | OAuth 플로우 구현 | BE | 2 | 🟠 High | ⬜ 예정 |
| **0.3.3** | 기반 | **암호화 설계** | 계좌번호, Access Token AES-256 암호화, Vault 설계 | app/core/encryption.py | BE | 2 | 🔴 Critical | ⬜ 예정 |

**📱 Phase 1\. 모바일 앱 \+ 금융 계좌 연동 (WP1 핵심)**

| ID | WP | 작업명 | 상세 내용 | 산출물 | 담당 | 주차 | 우선순위 | 상태 |
| :---: | :---: | ----- | ----- | ----- | :---: | :---: | :---: | :---: |
| **1.1.1** | WP1 | **모바일 앱 프레임워크 선택** | React Native vs Flutter 기술 검토, 초기 세팅, 네비게이션 구조 | 앱 초기 프로젝트 구조 | 앱 | 2 | 🔴 Critical | ⬜ 예정 |
| **1.1.2** | WP1 | **로그인 / 회원가입 UI** | 이메일+소셜 로그인, JWT 토큰 저장, 온보딩 플로우 | Auth 화면 완성 | 앱 | 3 | 🔴 Critical | ⬜ 예정 |
| **1.1.3** | WP1 | **계좌 연결 UI** | 오픈뱅킹 인증 흐름 UI, 기관 검색, 연결 성공/실패 처리 | 계좌연결 화면 | 앱 | 3 | 🔴 Critical | ⬜ 예정 |
| **1.2.1** | WP1.1 | **오픈뱅킹 API 연동** | 금융결제원 오픈뱅킹, Access Token 관리, 계좌 리스트 수집 | banking\_service.py | BE | 3 | 🔴 Critical | ⬜ 예정 |
| **1.2.2** | WP1.1 | **증권 API 연동** | 토스증권/키움 API, 보유종목/수익률 실시간 조회 | investment\_service.py | BE | 4 | 🟠 High | ⬜ 예정 |
| **1.2.3** | WP1.1 | **카드사 API 연동** | 주요 카드사 거래내역, 청구예정금액, 실적 조회 | card\_service.py | BE | 4 | 🟠 High | ⬜ 예정 |
| **1.2.4** | WP1.2 | **가상자산 거래소 연동** | 업비트/바이낸스 API, 코인 보유현황, 수익률 계산 | crypto\_service.py | BE | 5 | 🟡 Medium | ⬜ 예정 |
| **1.2.5** | WP1.3 | **포인트/마일리지 수집** | 주요 포인트 API 연동, 현금환산 로직 | points\_service.py | BE | 5 | 🟡 Medium | ⬜ 예정 |
| **1.3.1** | WP1 | **데이터 수집 파이프라인 (Pull)** | 주기적 동기화 Celery/APScheduler, 기관별 갱신 주기 설정 | app/tasks/sync\_tasks.py | BE | 4 | 🔴 Critical | ⬜ 예정 |
| **1.3.2** | WP1 | **Webhook Push 처리** | 거래 발생 즉시 수신, 이벤트 큐 투입, 중복 제거 로직 | app/api/webhooks.py | BE | 4 | 🟠 High | ⬜ 예정 |
| **1.3.3** | WP1 | **거래 내역 정규화** | 기관별 상이한 포맷 → 공통 Transaction 스키마 변환 | app/core/normalizer.py | BE | 4 | 🔴 Critical | ⬜ 예정 |
| **1.4.1** | WP1 | **Assets 테이블 설계/구현** | 멀티 기관 계좌 통합, 잔액 스냅샷, 자산 유형 분류 | assets 도메인 완성 | BE | 3 | 🔴 Critical | ⬜ 예정 |
| **1.4.2** | WP1 | **Transactions 테이블 설계/구현** | 원천 데이터, Category\_ID, Emotion\_Tag 컬럼 포함 | transactions 도메인 완성 | BE | 3 | 🔴 Critical | ⬜ 예정 |
| **1.5.1** | WP1.4 | **FDS 이상거래 감지 설계** | 평균 소비 패턴 대비 이상치 탐지 모델, 실시간 차단 흐름 | fds\_service.py | AI+BE | 6 | 🟠 High | ⬜ 예정 |
| **1.5.2** | WP1.5 | **사기 의심 계좌 탐지** | 금융사기 이력 DB 연동, 송금 전 실시간 조회 | fraud\_check\_service.py | BE | 6 | 🟠 High | ⬜ 예정 |
| **1.6.1** | WP1.7 | **멀티 디바이스 동기화 설계** | 워치/CarPlay 데이터 연동 구조 설계 (Phase 후반 구현) | sync\_protocol.md | 앱+BE | 10 | 🟢 Low | ⬜ 예정 |

**🔄 Phase 2\. n8n 워크플로우 자동화 (Automation Brain)**

| ID | WP | 작업명 | 상세 내용 | 산출물 | 담당 | 주차 | 우선순위 | 상태 |
| :---: | :---: | ----- | ----- | ----- | :---: | :---: | :---: | :---: |
| **2.1.1** | 자동화 | **n8n Docker 배포** | Docker Compose에 n8n 서비스 추가, 포트/볼륨 설정 | n8n 운영 환경 | DevOps | 2 | 🔴 Critical | ⬜ 예정 |
| **2.1.2** | 자동화 | **n8n ↔ FastAPI Webhook 연결** | FastAPI에서 n8n Webhook 호출, 인증 토큰 관리 | Webhook 양방향 연결 | BE | 3 | 🔴 Critical | ⬜ 예정 |
| **2.2.1** | WP3 | **"거래 발생" 이벤트 트리거** | 신규 Transaction 저장 시 n8n 트리거, 이벤트 라우팅 | transaction\_trigger 워크플로우 | BE+n8n | 5 | 🔴 Critical | ⬜ 예정 |
| **2.2.2** | WP3 | **"잔액 변화" 트리거** | 잔액 임계값 초과/미달 시 자동 알림 및 액션 발동 | balance\_alert 워크플로우 | BE+n8n | 5 | 🟠 High | ⬜ 예정 |
| **2.2.3** | WP3 | **"급격한 소비 증가" 트리거** | 단기간 소비 급증 패턴 탐지 → 개입 워크플로우 실행 | spending\_spike 워크플로우 | AI+n8n | 6 | 🟠 High | ⬜ 예정 |
| **2.3.1** | WP3.1 | **자동 이체 워크플로우** | 생활비/저축/비상금/투자 계좌 자동 분배 룰 엔진 | auto\_transfer 워크플로우 | n8n+BE | 6 | 🔴 Critical | ⬜ 예정 |
| **2.3.2** | WP3.3 | **비상금 파킹통장 자동 이동** | 유동 자금 → 파킹통장 자동 이체, 이자 극대화 로직 | emergency\_fund 워크플로우 | n8n | 7 | 🟠 High | ⬜ 예정 |
| **2.3.3** | WP3.7 | **저점 매수 자동화 트리거** | 증시 과매도 지표 조건 충족 시 투자 가이드 실행 | dip\_buying 워크플로우 | n8n+AI | 9 | 🟡 Medium | ⬜ 예정 |
| **2.4.1** | 자동화 | **알림 채널 연동 (Slack/이메일)** | n8n Slack/Gmail 노드 설정, 메시지 템플릿 구성 | 알림 워크플로우 3종 | n8n | 4 | 🟠 High | ⬜ 예정 |
| **2.4.2** | 자동화 | **카카오톡/푸시 알림 연동** | 카카오 알림톡 API, FCM 푸시 알림 n8n 노드 구성 | 푸시 알림 워크플로우 | n8n+앱 | 5 | 🟠 High | ⬜ 예정 |
| **2.5.1** | 자동화 | **n8n → FastAPI AI 에이전트 호출** | AI 판단이 필요한 시점에 n8n이 FastAPI LLM 엔드포인트 호출 | ai\_agent\_call 워크플로우 | n8n+AI | 7 | 🔴 Critical | ⬜ 예정 |

**🧠 Phase 3\. AI 분석 엔진 (Core Brain) \- WP2**

| ID | WP | 작업명 | 상세 내용 | 산출물 | 담당 | 주차 | 우선순위 | 상태 |
| :---: | :---: | ----- | ----- | ----- | :---: | :---: | :---: | :---: |
| **3.1.1** | WP2 | **거래 카테고리 자동 분류 (LLM)** | GPT-4o-mini 기반 소비 카테고리 99% 자동 매핑, 학습 루프 | category\_classifier.py | AI | 5 | 🔴 Critical | ⬜ 예정 |
| **3.1.2** | WP2 | **고정비 자동 탐지** | 구독/공과금/보험료 패턴 추출, 월별 고정 지출 리스트 자동 생성 | fixed\_cost\_detector.py | AI | 6 | 🟠 High | ⬜ 예정 |
| **3.1.3** | WP2 | **소비 패턴 군집화** | K-Means/DBSCAN으로 유사 소비 패턴 군집, 유사 그룹 비교 기반 | pattern\_clustering.py | AI | 7 | 🟡 Medium | ⬜ 예정 |
| **3.1.4** | WP2 | **이상치 탐지 모델** | Isolation Forest / Z-Score 기반 비정상 거래 탐지 | anomaly\_detector.py | AI | 6 | 🟠 High | ⬜ 예정 |
| **3.2.1** | WP2.3 | **현금 흐름 시각화 API** | Sankey 차트용 수입/지출 경로 데이터 집계 API 개발 | /api/analytics/cashflow | BE+AI | 6 | 🟠 High | ⬜ 예정 |
| **3.2.2** | WP2.4 | **미래 잔고 예측 모델** | 시계열(Prophet/LSTM) 기반 3\~6개월 잔고 시뮬레이션 | balance\_predictor.py | AI | 7 | 🟠 High | ⬜ 예정 |
| **3.2.3** | WP2.7 | **인플레이션 반영 자산 계산** | 소비자물가지수(CPI) API 연동, 실질 자산가치 변화 측정 | inflation\_adjuster.py | AI+BE | 8 | 🟡 Medium | ⬜ 예정 |
| **3.3.1** | WP2.5 | **뉴스 감정 분석 (보유 종목)** | 네이버/구글 뉴스 크롤링, BERT 감정분석, 포트폴리오 영향도 스코어링 | sentiment\_analyzer.py | AI | 8 | 🟡 Medium | ⬜ 예정 |
| **3.4.1** | WP2.6 | **대화형 인터페이스 (챗봇 API)** | "이번달 술값 얼마야?" 자연어 질의 → SQL 자동 생성 → 답변 | /api/chat/query | AI+BE | 7 | 🟠 High | ⬜ 예정 |
| **3.5.1** | WP2 | **포트폴리오 분석 엔진** | 자산 배분 현황, 변동성, 샤프지수 계산, 리밸런싱 제안 | portfolio\_analyzer.py | AI | 8 | 🟠 High | ⬜ 예정 |
| **3.5.2** | WP3.5 | **리밸런싱 알고리즘** | 목표 비중 대비 현재 비중 편차 계산, 최소 거래 비용 최적화 | rebalancer.py | AI | 9 | 🟡 Medium | ⬜ 예정 |

**💸 Phase 4\. 자동 자금 운영 시스템 (Execution Layer) \- WP3**

| ID | WP | 작업명 | 상세 내용 | 산출물 | 담당 | 주차 | 우선순위 | 상태 |
| :---: | :---: | ----- | ----- | ----- | :---: | :---: | :---: | :---: |
| **4.1.1** | WP3.1 | **룰 기반 자동 이체 엔진** | 사용자 정의 규칙(조건/금액/날짜)에 따른 자동 이체 실행 | transfer\_rule\_engine.py | BE | 6 | 🔴 Critical | ⬜ 예정 |
| **4.1.2** | WP3.1 | **AI 기반 이체 최적화** | 잔고 예측 기반 이체 시점/금액 자동 조정, 이자 손실 최소화 | smart\_transfer\_optimizer.py | AI+BE | 8 | 🟠 High | ⬜ 예정 |
| **4.2.1** | WP3.2 | **실시간 지출 피드백 시스템** | 결제 발생 즉시 AI 개입, 소비 적절성 평가, 예산 초과 경고 | spending\_feedback\_service.py | AI+BE | 7 | 🔴 Critical | ⬜ 예정 |
| **4.3.1** | WP3.4 | **ISA/IRP 최적화 엔진** | 세제 혜택 계산, 납입 한도 추적, 최적 납입 시점 가이드 | tax\_account\_optimizer.py | BE+AI | 9 | 🟡 Medium | ⬜ 예정 |
| **4.3.2** | WP5.7 | **연말정산 시뮬레이터** | 신용/체크카드 비중 실시간 계산, 공제 최적화 가이드 | /api/tax/year-end-sim | BE+AI | 10 | 🟡 Medium | ⬜ 예정 |
| **4.4.1** | WP3.6 | **카드 실적 계산기** | 혜택 충족 부족 금액 실시간 계산, 카드별 혜택 비교 | card\_benefit\_tracker.py | BE | 7 | 🟡 Medium | ⬜ 예정 |
| **4.5.1** | WP5.8 | **할부 누적 시각화** | 향후 n개월 고정 할부 지불 통합 경고, 가처분소득 예측 | /api/installment/forecast | BE | 8 | 🟡 Medium | ⬜ 예정 |
| **4.6.1** | WP1.6 | **신용 점수 모니터링 (KCB/NICE)** | 신용점수 변동 실시간 추적, 하락 요인 분석, 상승 가이드 | credit\_score\_service.py | BE+AI | 9 | 🟡 Medium | ⬜ 예정 |

**🧠 Phase 5\. 행동경제학 코치 시스템 (WP4 – 핵심 차별화)**

| ID | WP | 작업명 | 상세 내용 | 산출물 | 담당 | 주차 | 우선순위 | 상태 |
| :---: | :---: | ----- | ----- | ----- | :---: | :---: | :---: | :---: |
| **5.1.1** | WP4.1 | **상황별 소비 제안 AI** | "이 커피 마시면 여행 자금 부족" 등 맥락 기반 즉각 조언 | contextual\_advice.py | AI | 8 | 🔴 Critical | ⬜ 예정 |
| **5.1.2** | WP4.3 | **미래 가치 변환 엔진** | "지금 100만원 폰 → 10년 후 500만원 은퇴자금 손실" 계산 | future\_value\_converter.py | AI | 8 | 🟠 High | ⬜ 예정 |
| **5.1.3** | WP4.6 | **기회비용 보고 (택시/커피 등)** | 소비 항목을 자산 성장 관점으로 재프레이밍, 보고서 생성 | opportunity\_cost\_reporter.py | AI | 9 | 🟡 Medium | ⬜ 예정 |
| **5.2.1** | WP4.2 | **예산 초과 즉각 경고 시스템** | 카테고리별 예산 임박 시 강력 알림, 소비 중단 권고 메시지 | budget\_alert\_service.py | BE+AI | 7 | 🔴 Critical | ⬜ 예정 |
| **5.2.2** | WP4.5 | **구독 해지 권고 엔진** | 미사용 기간 감지, 유사 무료 서비스 대안 제안, 해지 가이드 | subscription\_advisor.py | AI+BE | 9 | 🟡 Medium | ⬜ 예정 |
| **5.3.1** | WP4.4 | **동기부여 메시지 생성 AI** | "점심값 아끼면 애플 주식 1주" 등 구체적 행동 유도 LLM 생성 | motivation\_engine.py | AI | 8 | 🟠 High | ⬜ 예정 |
| **5.3.2** | WP4.7 | **무지출 챌린지 시스템** | 지출 0원 날 달력 표시, 연속 달성 스트릭, 보너스 저축 유도 | zero\_spending\_tracker.py | BE+앱 | 9 | 🟡 Medium | ⬜ 예정 |

**📊 Phase 6\. 재무 건강 & 인생 로드맵 (WP5)**

| ID | WP | 작업명 | 상세 내용 | 산출물 | 담당 | 주차 | 우선순위 | 상태 |
| :---: | :---: | ----- | ----- | ----- | :---: | :---: | :---: | :---: |
| **6.1.1** | WP5.1 | **재무 건강 스코어 엔진** | 소비패턴/저축률/부채비율/투자성향 종합 점수 알고리즘 | financial\_health\_scorer.py | AI | 9 | 🔴 Critical | ⬜ 예정 |
| **6.1.2** | WP5.1 | **월간 종합 리포트 생성** | AI가 월말에 자동으로 재무 리포트 \+ 개선안 생성 및 발송 | monthly\_report\_generator.py | AI+BE | 10 | 🟠 High | ⬜ 예정 |
| **6.2.1** | WP5.2 | **유사 그룹 비교 분석** | 동일 소득/연령대 소비 패턴 벤치마킹, 익명화 처리 | peer\_comparison\_service.py | AI+BE | 10 | 🟡 Medium | ⬜ 예정 |
| **6.3.1** | WP5.3 | **목표 기반 저축 (Quest)** | 여행/자동차/집 목표 설정, 잔돈 모으기/정액 저축 연동 | quest\_savings\_service.py | BE | 9 | 🟠 High | ⬜ 예정 |
| **6.3.2** | WP5.4 | **자산 로드맵 게임화** | 5천만/1억 달성 퀘스트, 배지/보상 시스템, 진척도 시각화 | gamification\_engine.py | BE+앱 | 10 | 🟡 Medium | ⬜ 예정 |
| **6.4.1** | WP5.5 | **생애 주기 시나리오 시뮬레이터** | 결혼/출산/은퇴 이벤트별 비용 시뮬레이션, 준비 상태 점검 | lifecycle\_simulator.py | AI | 10 | 🟡 Medium | ⬜ 예정 |

**🐳 Phase 7\. Docker 기반 배포 및 운영 (DevOps)**

| ID | WP | 작업명 | 상세 내용 | 산출물 | 담당 | 주차 | 우선순위 | 상태 |
| :---: | :---: | ----- | ----- | ----- | :---: | :---: | :---: | :---: |
| **7.1.1** | DevOps | **전체 Docker Compose 완성** | FastAPI \+ PostgreSQL \+ Redis \+ n8n \+ Celery Worker 통합 구성 | docker-compose.prod.yml | DevOps | 3 | 🔴 Critical | ⬜ 예정 |
| **7.1.2** | DevOps | **환경변수 관리 체계** | .env 파일 구조화, Secret Manager 연동 (AWS/GCP) | .env.prod, secrets 설정 | DevOps | 3 | 🟠 High | ⬜ 예정 |
| **7.2.1** | DevOps | **AWS/GCP 배포 환경 구성** | EC2/GCE 인스턴스, VPC, 보안그룹, 로드밸런서 설정 | 클라우드 인프라 완성 | DevOps | 4 | 🟠 High | ⬜ 예정 |
| **7.2.2** | DevOps | **HTTPS / 도메인 설정** | Nginx 리버스 프록시, Let's Encrypt SSL, 도메인 연결 | HTTPS 운영 환경 | DevOps | 4 | 🔴 Critical | ⬜ 예정 |
| **7.3.1** | DevOps | **로그 모니터링 구축** | Grafana \+ Loki 또는 ELK 스택, 에러/성능 알림 설정 | 모니터링 대시보드 | DevOps | 6 | 🟠 High | ⬜ 예정 |
| **7.4.1** | DevOps | **Auto Scaling 설정** | 트래픽 기반 자동 확장, Worker 분리 배포 | Auto Scaling 정책 | DevOps | 8 | 🟡 Medium | ⬜ 예정 |
| **7.5.1** | DevOps | **실시간 이벤트 스트리밍 (Kafka)** | Kafka/Redis Stream 설치, 거래 이벤트 토픽 설계, Consumer 구현 | event\_streaming 인프라 | BE+DevOps | 7 | 🟠 High | ⬜ 예정 |

**🧪 Phase 8\. 테스트 및 품질 관리**

| ID | WP | 작업명 | 상세 내용 | 산출물 | 담당 | 주차 | 우선순위 | 상태 |
| :---: | :---: | ----- | ----- | ----- | :---: | :---: | :---: | :---: |
| **8.1.1** | QA | **단위 테스트 작성 (pytest)** | 각 도메인 Service/Repository 단위 테스트, 커버리지 80% 목표 | tests/unit/ | 전체 | 지속 | 🟠 High | ⬜ 예정 |
| **8.1.2** | QA | **통합 테스트** | API 엔드포인트 E2E 테스트, DB 통합 테스트, n8n 워크플로우 검증 | tests/integration/ | 전체 | 지속 | 🟠 High | ⬜ 예정 |
| **8.1.3** | QA | **금융 시나리오 테스트** | 자동이체/리밸런싱/FDS 실제 시나리오 기반 테스트 케이스 | tests/scenarios/ | QA+BE | 9-10 | 🔴 Critical | ⬜ 예정 |
| **8.1.4** | QA | **보안 테스트** | SQL Injection, JWT 탈취, 암호화 취약점 점검 | 보안 점검 보고서 | 전체 | 10 | 🔴 Critical | ⬜ 예정 |

# **📅 10주 구현 로드맵 (타임라인)**

| 주차 | 마일스톤 | 주요 산출물 |
| :---: | ----- | ----- |
| **1주차** | **🧱 기반 환경 완성** | Docker Compose, DB 연결, 도메인 스캐폴딩, JWT 인증 |
| **2주차** | **🔐 보안+n8n 기반** | OAuth, 암호화, n8n 배포, 이벤트 구조 설계 |
| **3주차** | **📱 앱 \+ 오픈뱅킹 연동** | 모바일 앱 로그인, 오픈뱅킹 API, Assets/Transactions DB |
| **4주차** | **🔗 금융 API 전체 연동** | 증권/카드 API, 데이터 파이프라인, Webhook, 알림 채널 |
| **5주차** | **🤖 이벤트 자동화 가동** | n8n 트리거 3종, 가상자산/포인트 연동, LLM 분류기 |
| **6주차** | **💸 자금 운영 엔진** | 자동이체 룰엔진, FDS/사기탐지, 현금흐름 API, 소비 피드백 |
| **7주차** | **🧠 AI 엔진 핵심 완성** | 챗봇 API, 잔고 예측, 카드 실적, 예산 경고, Kafka |
| **8주차** | **📊 분석+코치 고도화** | 포트폴리오 분석, 감정분석, AI 코치, 모티베이션, Auto Scaling |
| **9주차** | **🎮 게임화+절세** | 퀘스트 저축, ISA/IRP, 신용점수, 구독 해지, 무지출 챌린지 |
| **10주차** | **🏁 완성 및 품질 보증** | 월간 리포트, 생애 시뮬레이터, 연말정산, 보안 테스트, 런칭 |

# **🏗️ 시스템 아키텍처 데이터 흐름**

| 단계 | 레이어 | 설명 |
| :---: | ----- | ----- |
| **①** | **모바일 앱** | 사용자 인터페이스 / 금융 계좌 연결 (오픈뱅킹 OAuth) |
| **②** | **FastAPI 서버** | 비즈니스 로직 / 도메인 분리 Layered Architecture |
| **③** | **PostgreSQL DB** | 자산/거래/사용자/자동화 데이터 영구 저장 |
| **④** | **AI 분석 엔진** | LLM 분류 / 예측 / 감정분석 / 행동 코칭 |
| **⑤** | **n8n 자동화** | 이벤트 트리거 → 워크플로우 실행 → 자동 이체/알림 |
| **⑥** | **사용자 행동 개입** | 실시간 피드백 / 코칭 메시지 / 동기부여 → 앱으로 반환 |

# **🗄️ 핵심 DB 테이블 (ERD 설계 가이드)**

| 테이블 | PK | 주요 컬럼 | 관계 |
| ----- | ----- | ----- | ----- |
| **users** | id (UUID) | email, name, risk\_profile, credit\_score, quest\_state | assets, transactions, automations 참조 |
| **assets** | id (UUID) | user\_id, institution, account\_type, balance, currency, last\_synced | user\_id → users |
| **transactions** | id (UUID) | user\_id, asset\_id, amount, merchant, category\_id, emotion\_tag, raw\_data | asset\_id → assets |
| **automations** | id (UUID) | user\_id, rule\_type, condition\_json, action\_json, is\_active | user\_id → users |
| **investment\_portfolio** | id (UUID) | user\_id, ticker, quantity, avg\_price, current\_price, allocation\_pct | user\_id → users |
| **user\_goals (quests)** | id (UUID) | user\_id, goal\_type, target\_amount, current\_amount, deadline, status | user\_id → users |
| **ai\_insights** | id (UUID) | user\_id, insight\_type, message, confidence, action\_taken, created\_at | user\_id → users |

**✅ 구현 핵심 원칙**

* ① Phase 0 완전 완료 후 Phase 1 진입 — 기반 없이 상위 기능 구현 금지  
* ② generate\_finance\_domain.py 활용 — 도메인 스캐폴딩 자동화로 일관된 구조 유지  
* ③ 테스트 코드 동시 작성 — 구현과 테스트를 동일 주차에 진행  
* ④ 금융 데이터 먼저, AI는 두 번째 — 실제 데이터 파이프라인 완성 후 AI 모델 연결  
* ⑤ 매주 Docker 빌드 통과 검증 — CI/CD로 항상 배포 가능한 상태 유지