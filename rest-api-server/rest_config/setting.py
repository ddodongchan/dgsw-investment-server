from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    INTERNAL_API_KEY: str
    DATABASE_URL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Settings 인스턴스를 생성하고 확인
settings = Settings()
