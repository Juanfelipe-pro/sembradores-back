from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "Sembradores de Fe"
    DEBUG: bool = True
    DATABASE_URL: str
    SECRET_KEY: str
    ALLOWED_ORIGINS: str = "http://localhost:3000"
    FRONTEND_URL: str = "http://localhost:3000"
    ADMIN_EMAIL: str = "admin@sembradoresdefe.com"
    ADMIN_PASSWORD: str = "Admin123!"
    
    # Google OAuth
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    
    # MercadoPago
    MP_ACCESS_TOKEN: str = ""
    MP_PUBLIC_KEY: str = ""
    
    # Web Push
    VAPID_PUBLIC_KEY: str = ""
    VAPID_PRIVATE_KEY: str = ""
    VAPID_CLAIM_EMAIL: str = "mailto:admin@sembradoresdefe.com"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"  # Ignorar campos extra del .env
    )
    
    @property
    def allowed_origins_list(self):
        return [o.strip() for o in self.ALLOWED_ORIGINS.split(",")]

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()