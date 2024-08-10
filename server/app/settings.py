from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_LIFETIME_SECONDS: int = 3600
    BOT_TOKEN: str | None = None
    ADMIN_CHAT_ID: str | None = None


settings = Settings()
