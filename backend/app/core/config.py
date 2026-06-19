from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    APP_NAME: str = "AI Concierge"

    DATABASE_URL: str

    SECRET_KEY: str

    GEMINI_API_KEY: str

    QDRANT_URL: str

    class Config:
        env_file = ".env"


settings = Settings()
