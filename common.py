"""
Common utilities cho Bài 1 và Bài 5
"""
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()


class Config:
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    GOOGLE_MODEL: str = os.getenv("GOOGLE_MODEL", "gemini-2.5-flash")
    
    @classmethod
    def reload(cls):
        load_dotenv(override=True)
        cls.GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
        cls.GOOGLE_MODEL = os.getenv("GOOGLE_MODEL", "gemini-2.5-flash")
    
    @classmethod
    def validate(cls):
        if not cls.GOOGLE_API_KEY:
            raise ValueError(
                "Chưa có GOOGLE_API_KEY trong file .env\n"
                "Tạo file .env và thêm: GOOGLE_API_KEY=your_key\n"
                "Lấy key tại: https://makersuite.google.com/app/apikey"
            )
        return True


class GoogleAIService:
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.client = genai.Client(api_key=api_key)
    
    def reload_api_key(self, new_key: str):
        if new_key != self.api_key:
            self.api_key = new_key
            self.client = genai.Client(api_key=new_key)

