# app/core/ai_client.py
import logging
import google.generativeai as genai
from app.core.config import settings

logger = logging.getLogger(__name__)

class GeminiClient:
    def __init__(self):
        self._model = None

    def _get_model(self):
        if not self._model:
            if not settings.GEMINI_API_KEY:
                raise RuntimeError("GEMINI_API_KEY가 설정되지 않았습니다.")
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self._model = genai.GenerativeModel("models/gemini-2.5-flash-lite")
        return self._model

    async def generate(self, prompt: str) -> str:
        model = self._get_model()
        response = await model.generate_content_async(prompt)
        return response.text.strip()
    
gemini_client = GeminiClient()