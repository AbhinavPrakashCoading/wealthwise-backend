from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache
import os

class Settings(BaseSettings):
    ENV: str = "development"
    SECRET_KEY: str = "change_me"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DATABASE_URL: str = "sqlite:///./wealthwise.db"
    CORS_ORIGINS: str = "http://localhost:5173"
    ZERODHA_API_KEY: str = ""
    ZERODHA_API_SECRET: str = ""
    AA_CLIENT_ID: str = ""
    AA_CLIENT_SECRET: str = ""

    class Config:
        env_file = ".env"

    def cors_list(self) -> List[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]

@lru_cache
def get_settings():
    return Settings()
