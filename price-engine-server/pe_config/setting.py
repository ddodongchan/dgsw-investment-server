from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    redis_stream_host: str
    redis_stream_port: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Settings 인스턴스를 생성하고 확인
settings = Settings()