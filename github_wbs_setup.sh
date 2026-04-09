#!/bin/bash
# ============================================================
# AI 금융 비서 (Finance OS) - GitHub WBS 자동 생성 스크립트
# ============================================================
# 사전 준비:
#   1. GitHub CLI 설치: brew install gh (macOS) / winget install GitHub.cli (Windows)
#   2. 로그인: gh auth login
#   3. 레포 생성 후 이 스크립트를 레포 루트에서 실행
#
# 실행 방법:
#   chmod +x github_wbs_setup.sh
#   ./github_wbs_setup.sh
# ============================================================

set -e

# ── 색상 출력 ──────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; CYAN='\033[0;36m'; BOLD='\033[1m'; NC='\033[0m'

echo -e "${BOLD}${BLUE}"
echo "╔══════════════════════════════════════════════════════╗"
echo "║   🏦 AI 금융 비서 Finance OS - GitHub WBS 자동 생성  ║"
echo "╚══════════════════════════════════════════════════════╝"
echo -e "${NC}"

# ── 환경 확인 ──────────────────────────────────────────────
if ! command -v gh &> /dev/null; then
  echo -e "${RED}❌ GitHub CLI(gh)가 설치되어 있지 않습니다.${NC}"
  echo "   macOS:   brew install gh"
  echo "   Windows: winget install GitHub.cli"
  echo "   Linux:   https://github.com/cli/cli#installation"
  exit 1
fi

if ! gh auth status &> /dev/null; then
  echo -e "${RED}❌ GitHub 로그인이 필요합니다. 'gh auth login'을 먼저 실행하세요.${NC}"
  exit 1
fi

# ── 레포 정보 확인 ──────────────────────────────────────────
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo "")
if [ -z "$REPO" ]; then
  echo -e "${RED}❌ GitHub 레포지토리를 찾을 수 없습니다.${NC}"
  echo "   레포 루트 디렉토리에서 실행하거나 'gh repo create'로 먼저 레포를 만드세요."
  exit 1
fi

OWNER=$(echo $REPO | cut -d'/' -f1)
echo -e "${GREEN}✅ 레포 확인: ${BOLD}$REPO${NC}"
echo ""

# ── 라벨 생성 ──────────────────────────────────────────────
echo -e "${CYAN}📌 라벨 생성 중...${NC}"

create_label() {
  local name="$1" color="$2" desc="$3"
  gh label create "$name" --color "$color" --description "$desc" --force 2>/dev/null || true
}

# Phase 라벨
create_label "Phase 0: 기반세팅"   "1B3A6B" "개발환경, Docker, 인증 기반"
create_label "Phase 1: 금융연동"   "065F46" "모바일앱, 오픈뱅킹, 데이터파이프라인"
create_label "Phase 2: n8n자동화"  "6D28D9" "워크플로우, 이벤트트리거, 알림"
create_label "Phase 3: AI분석"     "92400E" "LLM분류, 예측모델, 챗봇"
create_label "Phase 4: 자금운영"   "991B1B" "자동이체, 실시간피드백, 절세"
create_label "Phase 5: 행동코치"   "1D4ED8" "행동경제학, 소비개입, 동기부여"
create_label "Phase 6: 재무로드맵" "0E7490" "재무스코어, 게임화, 생애시뮬"
create_label "Phase 7: DevOps"     "374151" "Docker배포, 클라우드, 모니터링"
create_label "Phase 8: 테스트"     "4B5563" "단위테스트, 통합테스트, 보안"

# 우선순위 라벨
create_label "🔴 Critical" "DC2626" "즉시 구현 필수"
create_label "🟠 High"     "D97706" "높은 우선순위"
create_label "🟡 Medium"   "CA8A04" "중간 우선순위"
create_label "🟢 Low"      "059669" "낮은 우선순위"

# 담당 라벨
create_label "담당: BE"      "BBF7D0" "백엔드"
create_label "담당: AI"      "FDE68A" "AI/ML"
create_label "담당: 앱"      "DDD6FE" "모바일앱"
create_label "담당: DevOps"  "E5E7EB" "인프라/배포"
create_label "담당: QA"      "FEE2E2" "테스트/품질"
create_label "담당: n8n"     "FBCFE8" "자동화워크플로우"
create_label "담당: 전체"    "BFDBFE" "전체팀"

echo -e "${GREEN}✅ 라벨 생성 완료${NC}"
echo ""

# ── GitHub Project 생성 ─────────────────────────────────────
echo -e "${CYAN}🗂️  GitHub Project 생성 중...${NC}"
PROJECT_URL=$(gh project create --owner "$OWNER" --title "🏦 AI 금융 비서 (Finance OS) WBS" --format json 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('url',''))" 2>/dev/null || echo "")
if [ -n "$PROJECT_URL" ]; then
  echo -e "${GREEN}✅ Project 생성: $PROJECT_URL${NC}"
else
  echo -e "${YELLOW}⚠️  Project 자동 생성 실패 (권한 문제일 수 있음). Issue는 계속 생성됩니다.${NC}"
fi
echo ""

# ── Issue 생성 함수 ─────────────────────────────────────────
ISSUE_COUNT=0
create_issue() {
  local id="$1" title="$2" phase_label="$3" priority="$4" owner_label="$5"
  local week="$6" wp="$7" output="$8" detail="$9"

  local body="## 📋 태스크 정보

| 항목 | 내용 |
|------|------|
| **WBS ID** | \`$id\` |
| **Work Package** | $wp |
| **구현 주차** | $week |
| **담당** | $owner_label |
| **산출물** | \`$output\` |

## 📝 상세 내용

$detail

## ✅ 완료 조건 (Definition of Done)

- [ ] 코드 구현 완료
- [ ] 단위 테스트 작성 (커버리지 80% 이상)
- [ ] PR 리뷰 통과
- [ ] 산출물 파일 생성 확인
- [ ] 문서 업데이트"

  gh issue create \
    --title "[$id] $title" \
    --body "$body" \
    --label "$phase_label" \
    --label "$priority" \
    --label "담당: $owner_label" \
    > /dev/null 2>&1

  ISSUE_COUNT=$((ISSUE_COUNT + 1))
  echo -e "  ${GREEN}✓${NC} [$id] $title"
}

# ══════════════════════════════════════════════════════════════
# Phase 0: 프로젝트 기반 세팅
# ══════════════════════════════════════════════════════════════
echo -e "${BOLD}${BLUE}🧱 Phase 0. 프로젝트 기반 세팅 (11개)${NC}"

create_issue "0.1.1" "개발 환경 구성" "Phase 0: 기반세팅" "🔴 Critical" "전체" "1주차" "기반" "requirements.txt, .env.example" "Python 3.12, FastAPI, 가상환경(venv/pyenv) 세팅"
create_issue "0.1.2" "PostgreSQL / Supabase 연결" "Phase 0: 기반세팅" "🔴 Critical" "BE" "1주차" "기반" "app/core/database.py" "DB 연결, SessionLocal, Base 설정 (database.py)"
create_issue "0.1.3" "Redis 세팅" "Phase 0: 기반세팅" "🟠 High" "BE" "1주차" "기반" "app/core/cache.py" "캐시 및 큐용 Redis 연결 설정, 세션/토큰 캐싱 구조"
create_issue "0.1.4" "Docker Compose 구성" "Phase 0: 기반세팅" "🔴 Critical" "DevOps" "1주차" "기반" "docker-compose.yml" "FastAPI + PostgreSQL + Redis + n8n 컨테이너 정의"
create_issue "0.1.5" "GitHub Actions CI/CD" "Phase 0: 기반세팅" "🟠 High" "DevOps" "1주차" "기반" ".github/workflows/" "PR → 테스트 자동화, main 브랜치 배포 파이프라인"
create_issue "0.2.1" "Layered Architecture 설계" "Phase 0: 기반세팅" "🔴 Critical" "전체" "1주차" "기반" "아키텍처 문서, generate_finance_domain.py 실행" "Controller/Service/Repository 레이어 분리, 도메인 구조 확정"
create_issue "0.2.2" "도메인 스캐폴딩 실행" "Phase 0: 기반세팅" "🔴 Critical" "BE" "1주차" "기반" "app/domains/ 전체 구조" "users, assets, transactions, automation, investment, coach, planning 도메인 자동 생성"
create_issue "0.2.3" "이벤트 기반 구조 설계" "Phase 0: 기반세팅" "🟠 High" "BE" "2주차" "기반" "이벤트 설계 문서" "Pub/Sub 패턴, 도메인 이벤트 정의, Kafka/Redis Stream 선택"
create_issue "0.3.1" "JWT 인증 구현" "Phase 0: 기반세팅" "🔴 Critical" "BE" "2주차" "기반" "app/core/auth.py" "액세스/리프레시 토큰, 미들웨어 보안 설정"
create_issue "0.3.2" "OAuth 연동" "Phase 0: 기반세팅" "🟠 High" "BE" "2주차" "기반" "OAuth 플로우 구현" "카카오/네이버 소셜 로그인, 금융 API 인증 흐름"
create_issue "0.3.3" "암호화 설계" "Phase 0: 기반세팅" "🔴 Critical" "BE" "2주차" "기반" "app/core/encryption.py" "계좌번호, Access Token AES-256 암호화, Vault 설계"

# ══════════════════════════════════════════════════════════════
# Phase 1: 모바일 앱 + 금융 계좌 연동
# ══════════════════════════════════════════════════════════════
echo -e "\n${BOLD}${GREEN}📱 Phase 1. 모바일 앱 + 금융 계좌 연동 (16개)${NC}"

create_issue "1.1.1" "모바일 앱 프레임워크 선택" "Phase 1: 금융연동" "🔴 Critical" "앱" "2주차" "WP1" "앱 초기 프로젝트 구조" "React Native vs Flutter 기술 검토, 초기 세팅, 네비게이션 구조"
create_issue "1.1.2" "로그인 / 회원가입 UI" "Phase 1: 금융연동" "🔴 Critical" "앱" "3주차" "WP1" "Auth 화면 완성" "이메일+소셜 로그인, JWT 토큰 저장, 온보딩 플로우"
create_issue "1.1.3" "계좌 연결 UI" "Phase 1: 금융연동" "🔴 Critical" "앱" "3주차" "WP1" "계좌연결 화면" "오픈뱅킹 인증 흐름 UI, 기관 검색, 연결 성공/실패 처리"
create_issue "1.2.1" "오픈뱅킹 API 연동" "Phase 1: 금융연동" "🔴 Critical" "BE" "3주차" "WP1.1" "banking_service.py" "금융결제원 오픈뱅킹, Access Token 관리, 계좌 리스트 수집"
create_issue "1.2.2" "증권 API 연동" "Phase 1: 금융연동" "🟠 High" "BE" "4주차" "WP1.1" "investment_service.py" "토스증권/키움 API, 보유종목/수익률 실시간 조회"
create_issue "1.2.3" "카드사 API 연동" "Phase 1: 금융연동" "🟠 High" "BE" "4주차" "WP1.1" "card_service.py" "주요 카드사 거래내역, 청구예정금액, 실적 조회"
create_issue "1.2.4" "가상자산 거래소 연동" "Phase 1: 금융연동" "🟡 Medium" "BE" "5주차" "WP1.2" "crypto_service.py" "업비트/바이낸스 API, 코인 보유현황, 수익률 계산"
create_issue "1.2.5" "포인트/마일리지 수집" "Phase 1: 금융연동" "🟡 Medium" "BE" "5주차" "WP1.3" "points_service.py" "주요 포인트 API 연동, 현금환산 로직"
create_issue "1.3.1" "데이터 수집 파이프라인 (Pull)" "Phase 1: 금융연동" "🔴 Critical" "BE" "4주차" "WP1" "app/tasks/sync_tasks.py" "주기적 동기화 Celery/APScheduler, 기관별 갱신 주기 설정"
create_issue "1.3.2" "Webhook Push 처리" "Phase 1: 금융연동" "🟠 High" "BE" "4주차" "WP1" "app/api/webhooks.py" "거래 발생 즉시 수신, 이벤트 큐 투입, 중복 제거 로직"
create_issue "1.3.3" "거래 내역 정규화" "Phase 1: 금융연동" "🔴 Critical" "BE" "4주차" "WP1" "app/core/normalizer.py" "기관별 상이한 포맷 → 공통 Transaction 스키마 변환"
create_issue "1.4.1" "Assets 테이블 설계/구현" "Phase 1: 금융연동" "🔴 Critical" "BE" "3주차" "WP1" "assets 도메인 완성" "멀티 기관 계좌 통합, 잔액 스냅샷, 자산 유형 분류"
create_issue "1.4.2" "Transactions 테이블 설계/구현" "Phase 1: 금융연동" "🔴 Critical" "BE" "3주차" "WP1" "transactions 도메인 완성" "원천 데이터, Category_ID, Emotion_Tag 컬럼 포함"
create_issue "1.5.1" "FDS 이상거래 감지 설계" "Phase 1: 금융연동" "🟠 High" "BE" "6주차" "WP1.4" "fds_service.py" "평균 소비 패턴 대비 이상치 탐지 모델, 실시간 차단 흐름"
create_issue "1.5.2" "사기 의심 계좌 탐지" "Phase 1: 금융연동" "🟠 High" "BE" "6주차" "WP1.5" "fraud_check_service.py" "금융사기 이력 DB 연동, 송금 전 실시간 조회"
create_issue "1.6.1" "멀티 디바이스 동기화 설계" "Phase 1: 금융연동" "🟢 Low" "앱" "10주차" "WP1.7" "sync_protocol.md" "워치/CarPlay 데이터 연동 구조 설계"

# ══════════════════════════════════════════════════════════════
# Phase 2: n8n 자동화
# ══════════════════════════════════════════════════════════════
echo -e "\n${BOLD}${BLUE}🔄 Phase 2. n8n 워크플로우 자동화 (11개)${NC}"

create_issue "2.1.1" "n8n Docker 배포" "Phase 2: n8n자동화" "🔴 Critical" "DevOps" "2주차" "자동화" "n8n 운영 환경" "Docker Compose에 n8n 서비스 추가, 포트/볼륨 설정"
create_issue "2.1.2" "n8n ↔ FastAPI Webhook 연결" "Phase 2: n8n자동화" "🔴 Critical" "BE" "3주차" "자동화" "Webhook 양방향 연결" "FastAPI에서 n8n Webhook 호출, 인증 토큰 관리"
create_issue "2.2.1" "\"거래 발생\" 이벤트 트리거" "Phase 2: n8n자동화" "🔴 Critical" "n8n" "5주차" "WP3" "transaction_trigger 워크플로우" "신규 Transaction 저장 시 n8n 트리거, 이벤트 라우팅"
create_issue "2.2.2" "\"잔액 변화\" 트리거" "Phase 2: n8n자동화" "🟠 High" "n8n" "5주차" "WP3" "balance_alert 워크플로우" "잔액 임계값 초과/미달 시 자동 알림 및 액션 발동"
create_issue "2.2.3" "\"급격한 소비 증가\" 트리거" "Phase 2: n8n자동화" "🟠 High" "n8n" "6주차" "WP3" "spending_spike 워크플로우" "단기간 소비 급증 패턴 탐지 → 개입 워크플로우 실행"
create_issue "2.3.1" "자동 이체 워크플로우" "Phase 2: n8n자동화" "🔴 Critical" "n8n" "6주차" "WP3.1" "auto_transfer 워크플로우" "생활비/저축/비상금/투자 계좌 자동 분배 룰 엔진"
create_issue "2.3.2" "비상금 파킹통장 자동 이동" "Phase 2: n8n자동화" "🟠 High" "n8n" "7주차" "WP3.3" "emergency_fund 워크플로우" "유동 자금 → 파킹통장 자동 이체, 이자 극대화 로직"
create_issue "2.3.3" "저점 매수 자동화 트리거" "Phase 2: n8n자동화" "🟡 Medium" "n8n" "9주차" "WP3.7" "dip_buying 워크플로우" "증시 과매도 지표 조건 충족 시 투자 가이드 실행"
create_issue "2.4.1" "알림 채널 연동 (Slack/이메일)" "Phase 2: n8n자동화" "🟠 High" "n8n" "4주차" "자동화" "알림 워크플로우 3종" "n8n Slack/Gmail 노드 설정, 메시지 템플릿 구성"
create_issue "2.4.2" "카카오톡/푸시 알림 연동" "Phase 2: n8n자동화" "🟠 High" "n8n" "5주차" "자동화" "푸시 알림 워크플로우" "카카오 알림톡 API, FCM 푸시 알림 n8n 노드 구성"
create_issue "2.5.1" "n8n → FastAPI AI 에이전트 호출" "Phase 2: n8n자동화" "🔴 Critical" "n8n" "7주차" "자동화" "ai_agent_call 워크플로우" "AI 판단이 필요한 시점에 n8n이 FastAPI LLM 엔드포인트 호출"

# ══════════════════════════════════════════════════════════════
# Phase 3: AI 분석 엔진
# ══════════════════════════════════════════════════════════════
echo -e "\n${BOLD}${YELLOW}🧠 Phase 3. AI 분석 엔진 (11개)${NC}"

create_issue "3.1.1" "거래 카테고리 자동 분류 (LLM)" "Phase 3: AI분석" "🔴 Critical" "AI" "5주차" "WP2" "category_classifier.py" "GPT-4o-mini 기반 소비 카테고리 99% 자동 매핑, 학습 루프"
create_issue "3.1.2" "고정비 자동 탐지" "Phase 3: AI분석" "🟠 High" "AI" "6주차" "WP2" "fixed_cost_detector.py" "구독/공과금/보험료 패턴 추출, 월별 고정 지출 리스트 자동 생성"
create_issue "3.1.3" "소비 패턴 군집화" "Phase 3: AI분석" "🟡 Medium" "AI" "7주차" "WP2" "pattern_clustering.py" "K-Means/DBSCAN으로 유사 소비 패턴 군집, 유사 그룹 비교 기반"
create_issue "3.1.4" "이상치 탐지 모델" "Phase 3: AI분석" "🟠 High" "AI" "6주차" "WP2" "anomaly_detector.py" "Isolation Forest / Z-Score 기반 비정상 거래 탐지"
create_issue "3.2.1" "현금 흐름 시각화 API" "Phase 3: AI분석" "🟠 High" "BE" "6주차" "WP2.3" "/api/analytics/cashflow" "Sankey 차트용 수입/지출 경로 데이터 집계 API 개발"
create_issue "3.2.2" "미래 잔고 예측 모델" "Phase 3: AI분석" "🟠 High" "AI" "7주차" "WP2.4" "balance_predictor.py" "시계열(Prophet/LSTM) 기반 3~6개월 잔고 시뮬레이션"
create_issue "3.2.3" "인플레이션 반영 자산 계산" "Phase 3: AI분석" "🟡 Medium" "AI" "8주차" "WP2.7" "inflation_adjuster.py" "소비자물가지수(CPI) API 연동, 실질 자산가치 변화 측정"
create_issue "3.3.1" "뉴스 감정 분석 (보유 종목)" "Phase 3: AI분석" "🟡 Medium" "AI" "8주차" "WP2.5" "sentiment_analyzer.py" "네이버/구글 뉴스 크롤링, BERT 감정분석, 포트폴리오 영향도 스코어링"
create_issue "3.4.1" "대화형 인터페이스 (챗봇 API)" "Phase 3: AI분석" "🟠 High" "AI" "7주차" "WP2.6" "/api/chat/query" "\"이번달 술값 얼마야?\" 자연어 질의 → SQL 자동 생성 → 답변"
create_issue "3.5.1" "포트폴리오 분석 엔진" "Phase 3: AI분석" "🟠 High" "AI" "8주차" "WP2" "portfolio_analyzer.py" "자산 배분 현황, 변동성, 샤프지수 계산, 리밸런싱 제안"
create_issue "3.5.2" "리밸런싱 알고리즘" "Phase 3: AI분석" "🟡 Medium" "AI" "9주차" "WP3.5" "rebalancer.py" "목표 비중 대비 현재 비중 편차 계산, 최소 거래 비용 최적화"

# ══════════════════════════════════════════════════════════════
# Phase 4: 자동 자금 운영 시스템
# ══════════════════════════════════════════════════════════════
echo -e "\n${BOLD}${RED}💸 Phase 4. 자동 자금 운영 시스템 (8개)${NC}"

create_issue "4.1.1" "룰 기반 자동 이체 엔진" "Phase 4: 자금운영" "🔴 Critical" "BE" "6주차" "WP3.1" "transfer_rule_engine.py" "사용자 정의 규칙(조건/금액/날짜)에 따른 자동 이체 실행"
create_issue "4.1.2" "AI 기반 이체 최적화" "Phase 4: 자금운영" "🟠 High" "BE" "8주차" "WP3.1" "smart_transfer_optimizer.py" "잔고 예측 기반 이체 시점/금액 자동 조정, 이자 손실 최소화"
create_issue "4.2.1" "실시간 지출 피드백 시스템" "Phase 4: 자금운영" "🔴 Critical" "BE" "7주차" "WP3.2" "spending_feedback_service.py" "결제 발생 즉시 AI 개입, 소비 적절성 평가, 예산 초과 경고"
create_issue "4.3.1" "ISA/IRP 최적화 엔진" "Phase 4: 자금운영" "🟡 Medium" "BE" "9주차" "WP3.4" "tax_account_optimizer.py" "세제 혜택 계산, 납입 한도 추적, 최적 납입 시점 가이드"
create_issue "4.3.2" "연말정산 시뮬레이터" "Phase 4: 자금운영" "🟡 Medium" "BE" "10주차" "WP5.7" "/api/tax/year-end-sim" "신용/체크카드 비중 실시간 계산, 공제 최적화 가이드"
create_issue "4.4.1" "카드 실적 계산기" "Phase 4: 자금운영" "🟡 Medium" "BE" "7주차" "WP3.6" "card_benefit_tracker.py" "혜택 충족 부족 금액 실시간 계산, 카드별 혜택 비교"
create_issue "4.5.1" "할부 누적 시각화" "Phase 4: 자금운영" "🟡 Medium" "BE" "8주차" "WP5.8" "/api/installment/forecast" "향후 n개월 고정 할부 지불 통합 경고, 가처분소득 예측"
create_issue "4.6.1" "신용 점수 모니터링 (KCB/NICE)" "Phase 4: 자금운영" "🟡 Medium" "BE" "9주차" "WP1.6" "credit_score_service.py" "신용점수 변동 실시간 추적, 하락 요인 분석, 상승 가이드"

# ══════════════════════════════════════════════════════════════
# Phase 5: 행동경제학 코치 시스템
# ══════════════════════════════════════════════════════════════
echo -e "\n${BOLD}${BLUE}🎯 Phase 5. 행동경제학 코치 시스템 (7개)${NC}"

create_issue "5.1.1" "상황별 소비 제안 AI" "Phase 5: 행동코치" "🔴 Critical" "AI" "8주차" "WP4.1" "contextual_advice.py" "\"이 커피 마시면 여행 자금 부족\" 등 맥락 기반 즉각 조언"
create_issue "5.1.2" "미래 가치 변환 엔진" "Phase 5: 행동코치" "🟠 High" "AI" "8주차" "WP4.3" "future_value_converter.py" "\"지금 100만원 폰 → 10년 후 500만원 은퇴자금 손실\" 계산"
create_issue "5.1.3" "기회비용 보고 (택시/커피 등)" "Phase 5: 행동코치" "🟡 Medium" "AI" "9주차" "WP4.6" "opportunity_cost_reporter.py" "소비 항목을 자산 성장 관점으로 재프레이밍, 보고서 생성"
create_issue "5.2.1" "예산 초과 즉각 경고 시스템" "Phase 5: 행동코치" "🔴 Critical" "BE" "7주차" "WP4.2" "budget_alert_service.py" "카테고리별 예산 임박 시 강력 알림, 소비 중단 권고 메시지"
create_issue "5.2.2" "구독 해지 권고 엔진" "Phase 5: 행동코치" "🟡 Medium" "AI" "9주차" "WP4.5" "subscription_advisor.py" "미사용 기간 감지, 유사 무료 서비스 대안 제안, 해지 가이드"
create_issue "5.3.1" "동기부여 메시지 생성 AI" "Phase 5: 행동코치" "🟠 High" "AI" "8주차" "WP4.4" "motivation_engine.py" "\"점심값 아끼면 애플 주식 1주\" 등 구체적 행동 유도 LLM 생성"
create_issue "5.3.2" "무지출 챌린지 시스템" "Phase 5: 행동코치" "🟡 Medium" "앱" "9주차" "WP4.7" "zero_spending_tracker.py" "지출 0원 날 달력 표시, 연속 달성 스트릭, 보너스 저축 유도"

# ══════════════════════════════════════════════════════════════
# Phase 6: 재무 건강 & 인생 로드맵
# ══════════════════════════════════════════════════════════════
echo -e "\n${BOLD}${CYAN}📊 Phase 6. 재무 건강 & 인생 로드맵 (6개)${NC}"

create_issue "6.1.1" "재무 건강 스코어 엔진" "Phase 6: 재무로드맵" "🔴 Critical" "AI" "9주차" "WP5.1" "financial_health_scorer.py" "소비패턴/저축률/부채비율/투자성향 종합 점수 알고리즘"
create_issue "6.1.2" "월간 종합 리포트 생성" "Phase 6: 재무로드맵" "🟠 High" "AI" "10주차" "WP5.1" "monthly_report_generator.py" "AI가 월말에 자동으로 재무 리포트 + 개선안 생성 및 발송"
create_issue "6.2.1" "유사 그룹 비교 분석" "Phase 6: 재무로드맵" "🟡 Medium" "AI" "10주차" "WP5.2" "peer_comparison_service.py" "동일 소득/연령대 소비 패턴 벤치마킹, 익명화 처리"
create_issue "6.3.1" "목표 기반 저축 (Quest)" "Phase 6: 재무로드맵" "🟠 High" "BE" "9주차" "WP5.3" "quest_savings_service.py" "여행/자동차/집 목표 설정, 잔돈 모으기/정액 저축 연동"
create_issue "6.3.2" "자산 로드맵 게임화" "Phase 6: 재무로드맵" "🟡 Medium" "BE" "10주차" "WP5.4" "gamification_engine.py" "5천만/1억 달성 퀘스트, 배지/보상 시스템, 진척도 시각화"
create_issue "6.4.1" "생애 주기 시나리오 시뮬레이터" "Phase 6: 재무로드맵" "🟡 Medium" "AI" "10주차" "WP5.5" "lifecycle_simulator.py" "결혼/출산/은퇴 이벤트별 비용 시뮬레이션, 준비 상태 점검"

# ══════════════════════════════════════════════════════════════
# Phase 7: Docker 기반 배포
# ══════════════════════════════════════════════════════════════
echo -e "\n${BOLD}${NC}🐳 Phase 7. Docker 기반 배포 및 운영 (7개)${NC}"

create_issue "7.1.1" "전체 Docker Compose 완성" "Phase 7: DevOps" "🔴 Critical" "DevOps" "3주차" "DevOps" "docker-compose.prod.yml" "FastAPI + PostgreSQL + Redis + n8n + Celery Worker 통합 구성"
create_issue "7.1.2" "환경변수 관리 체계" "Phase 7: DevOps" "🟠 High" "DevOps" "3주차" "DevOps" ".env.prod, secrets 설정" ".env 파일 구조화, Secret Manager 연동 (AWS/GCP)"
create_issue "7.2.1" "AWS/GCP 배포 환경 구성" "Phase 7: DevOps" "🟠 High" "DevOps" "4주차" "DevOps" "클라우드 인프라 완성" "EC2/GCE 인스턴스, VPC, 보안그룹, 로드밸런서 설정"
create_issue "7.2.2" "HTTPS / 도메인 설정" "Phase 7: DevOps" "🔴 Critical" "DevOps" "4주차" "DevOps" "HTTPS 운영 환경" "Nginx 리버스 프록시, Let's Encrypt SSL, 도메인 연결"
create_issue "7.3.1" "로그 모니터링 구축" "Phase 7: DevOps" "🟠 High" "DevOps" "6주차" "DevOps" "모니터링 대시보드" "Grafana + Loki 또는 ELK 스택, 에러/성능 알림 설정"
create_issue "7.4.1" "Auto Scaling 설정" "Phase 7: DevOps" "🟡 Medium" "DevOps" "8주차" "DevOps" "Auto Scaling 정책" "트래픽 기반 자동 확장, Worker 분리 배포"
create_issue "7.5.1" "실시간 이벤트 스트리밍 (Kafka)" "Phase 7: DevOps" "🟠 High" "BE" "7주차" "DevOps" "event_streaming 인프라" "Kafka/Redis Stream 설치, 거래 이벤트 토픽 설계, Consumer 구현"

# ══════════════════════════════════════════════════════════════
# Phase 8: 테스트 및 품질 관리
# ══════════════════════════════════════════════════════════════
echo -e "\n${BOLD}${NC}🧪 Phase 8. 테스트 및 품질 관리 (4개)${NC}"

create_issue "8.1.1" "단위 테스트 작성 (pytest)" "Phase 8: 테스트" "🟠 High" "QA" "지속" "QA" "tests/unit/" "각 도메인 Service/Repository 단위 테스트, 커버리지 80% 목표"
create_issue "8.1.2" "통합 테스트" "Phase 8: 테스트" "🟠 High" "QA" "지속" "QA" "tests/integration/" "API 엔드포인트 E2E 테스트, DB 통합 테스트, n8n 워크플로우 검증"
create_issue "8.1.3" "금융 시나리오 테스트" "Phase 8: 테스트" "🔴 Critical" "QA" "9-10주차" "QA" "tests/scenarios/" "자동이체/리밸런싱/FDS 실제 시나리오 기반 테스트 케이스"
create_issue "8.1.4" "보안 테스트" "Phase 8: 테스트" "🔴 Critical" "QA" "10주차" "QA" "보안 점검 보고서" "SQL Injection, JWT 탈취, 암호화 취약점 점검"

# ── 완료 메시지 ─────────────────────────────────────────────
echo ""
echo -e "${BOLD}${GREEN}"
echo "╔══════════════════════════════════════════════════════╗"
echo "║              ✅ WBS 생성 완료!                       ║"
echo "╚══════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo -e "📊 생성된 이슈: ${BOLD}${ISSUE_COUNT}개${NC}"
echo -e "🔗 레포지토리: ${BOLD}https://github.com/$REPO/issues${NC}"
if [ -n "$PROJECT_URL" ]; then
echo -e "🗂️  GitHub Project: ${BOLD}$PROJECT_URL${NC}"
fi
echo ""
echo -e "${YELLOW}💡 다음 단계:${NC}"
echo "  1. Issues 탭에서 생성된 80개 이슈 확인"
echo "  2. GitHub Projects에서 이슈를 Board/Table 뷰로 관리"
echo "  3. Milestone 생성: 1주차~10주차 (Settings > Milestones)"
echo "  4. 각 이슈에 Milestone 할당하여 주차별 관리"
echo ""
echo -e "${CYAN}📌 추천 설정:${NC}"
echo "  gh project view --owner $OWNER --web  # 프로젝트 웹에서 열기"
echo "  gh issue list --label '🔴 Critical'   # Critical 이슈만 보기"
echo "  gh issue list --label 'Phase 0: 기반세팅'  # Phase별 보기"
