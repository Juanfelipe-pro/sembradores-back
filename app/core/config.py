from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import secrets

class Settings(BaseSettings):
    APP_NAME: str = "Sembradores de Fe"
    DEBUG: bool = False
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/sembradores_fe"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALLOWED_ORIGINS: str = "http://localhost:3000"
    FRONTEND_URL: str = "http://localhost:3000"
    ADMIN_EMAIL: str = "admin@sembradoresdefe.com"
    ADMIN_PASSWORD: str = "Admin123!"
    
    # Google OAuth (opcional)
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    
    # MercadoPago (opcional)
    MP_ACCESS_TOKEN: str = ""
    MP_PUBLIC_KEY: str = ""
    
    # Web Push (opcional)
    VAPID_PUBLIC_KEY: str = ""
    VAPID_PRIVATE_KEY: str = ""
    VAPID_CLAIM_EMAIL: str = "mailto:admin@sembradoresdefe.com"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )
    
    @property
    def allowed_origins_list(self):
        return [o.strip() for o in self.ALLOWED_ORIGINS.split(",") if o.strip()]

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()