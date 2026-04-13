import google.generativeai as genai
import os
from dotenv import load_dotenv

# .env 파일의 환경 변수를 불러옵니다
load_dotenv()

# API 키 설정
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

print("--- 사용 가능한 모델 리스트 ---")
for m in genai.list_models():
    # 'generateContent'가 가능한 모델만 필터링해서 보여줍니다
    if 'generateContent' in m.supported_generation_methods:
        print(f"모델 이름: {m.name}")
        print(f"지원 기능: {m.supported_generation_methods}")
        print("-" * 30)