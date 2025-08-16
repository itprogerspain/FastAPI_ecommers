from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = "CHANGE_ME"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Настройки базы данных
    debug: bool
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int
    postgres_db: str

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
