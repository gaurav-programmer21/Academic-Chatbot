import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    MAX_HISTORY_LENGTH = 50
    MAX_KNOWLEDGE_ENTRIES = 100
    DEBUG = os.getenv('FLASK_ENV') == 'development'