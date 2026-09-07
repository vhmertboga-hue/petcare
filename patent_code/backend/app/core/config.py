from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "PetCarePlatform"
    VERSION: str = "0.1.0"
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@db:5432/petcare"
    REDIS_URL: str = "redis://redis:6379/0"
    S3_ENDPOINT: str = ""
    SECRET_KEY: str = "change-me"

    class Config:
        env_file = "../.env"


settings = Settings()
import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    # Default to a local SQLite DB for developer convenience. Production should
    # set DATABASE_URL to a Postgres (or other) URL in environment variables.
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+pysqlite:///./dev.db")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "replace-me")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "30"))
    debug: bool = os.getenv("PYTHON_ENV", "development") != "production"
    testing: bool = os.getenv("PYTHON_ENV", "development") == "test"

    def get_database_url(self) -> str:
        if self.testing:
            return os.getenv("TEST_DATABASE_URL", "sqlite+pysqlite:///:memory:")
        return self.DATABASE_URL


settings = Settings()
