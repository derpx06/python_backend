from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/taskapi"
    DATABASE_URL_SYNC: str = "postgresql://postgres:postgres@localhost:5432/taskapi"

    JWT_SECRET_KEY: str = "super-secret-jwt-key-change-in-production"
    JWT_REFRESH_SECRET_KEY: str = "super-secret-refresh-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    PORT: int = 4000
    ENVIRONMENT: str = "development"
    CORS_ORIGINS: str = "http://localhost:3000"

    ADMIN_EMAIL: str = "admin@taskapi.com"
    ADMIN_PASSWORD: str = "admin12345"
    ADMIN_NAME: str = "Admin User"

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
