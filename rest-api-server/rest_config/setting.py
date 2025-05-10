from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    internal_api_key: str
    database_url: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Settings 인스턴스를 생성하고 확인
settings = Settings()

print(settings.internal_api_key)
print(settings.database_url)
