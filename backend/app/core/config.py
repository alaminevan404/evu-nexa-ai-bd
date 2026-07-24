from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "EVU NEXA AI"
    VERSION: str = "2.4.0"
    API_V1_STR: str = "/api/v1"
    
    # Security Secrets
    SECRET_KEY: str = "EVU_NEXA_SUPER_SECRET_KEY_512_BITS_LONG_HMAC_RSA_2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_HOURS: int = 12
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    
    # Database Settings
    DATABASE_URL: str = "postgresql+asyncpg://evu_admin:NexaSecurePass2026!@localhost:5432/evu_nexa_db"
    
    # Redis Settings
    REDIS_URL: str = "redis://:RedisSecurePass2026!@localhost:6379/0"
    
    # Telegram Bot Configuration
    TELEGRAM_BOT_TOKEN: Optional[str] = "7000000000:AAFg_DummyTelegramBotTokenForDev"
    TELEGRAM_SUPPORT_USERNAME: str = "@et_evu"
    TELEGRAM_CHANNEL_ID: Optional[str] = "@evu_nexa_signals"
    
    # CORS Origins
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost",
        "http://localhost:80",
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ]

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
