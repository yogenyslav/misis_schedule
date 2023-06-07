from typing import Optional, Any
from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    DATABASE_URI: Optional[PostgresDsn] = None

    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v

        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=str(values.get("POSTGRES_HOST"))
            if values.get("POSTGRES_HOST")
            else "127.0.0.1",
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    DOCKER_MODE: bool
    LOGGING_LEVEL: str

    SCHEDULE_URL: str = "https://misis.ru/students/schedule/"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
