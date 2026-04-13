# app/domains/transaction/category_classifier.py
import logging
from app.core.ai_client import gemini_client

logger = logging.getLogger(__name__)

CATEGORIES = [
    "식비", "카페/음료", "교통", "쇼핑", "의료/건강", "문화/여가", "구독/OTT", "공과금/통신", "교육", "급여", "이자/배당", "이체", "기타"
]

PROMPT_TEMPLATE = """
당신은 금융 거래 데이터를 분류하는 전문가입니다.
아래 거래 정보를 보고 가장 적합한 카테고리 하나만 답하세요.

거래 정보:
- 가맹점/상호: {merchant}
- 메모: {description}
- 거래 유형: {transaction_type}
- 금액 : {amount}원

가능한 카테고리:
{categories}

규칙:
- 반드시 위 카테고리 중 하나만 정확히 답하세요.
- 다른 설명 없이 카테고리명만 답하세요.
""".strip()

async def classify_category(
        merchant: str | None,
        description: str | None,
        transaction_type: str,
        amount: str,
) -> str:
    if not merchant and not description:
        return "기타"
    
    prompt = PROMPT_TEMPLATE.format(
        merchant=merchant or "없음",
        description=description or "없음",
        transaction_type=transaction_type,
        amount=amount,
        categories="\n".join(f"- {c}" for c in CATEGORIES),
    )

    try:
        result = await gemini_client.generate(prompt)
        if result in CATEGORIES:
            return result
        for cat in CATEGORIES:
            if cat in result:
                return cat
        return "기타"
    except Exception as e:
        logger.error("카테고리 분류 실패 : %s", e)
        return "기타"