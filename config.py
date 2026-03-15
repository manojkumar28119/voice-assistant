# voice-assistant/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_SERVICE_ROLE_KEY: str
    SUPABASE_JWT_SECRET: str
    GROQ_API_KEY: str
    
    # Transcription/Speech Settings
    WHISPER_MODEL: str = "base"
    TTS_VOICE: str = "en-IN-NeerjaNeural"
    
    # Temporary Storage
    TEMP_DIR: str = "temp"
    RESPONSES_DIR: str = "responses"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
