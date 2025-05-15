from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    internal_api_key: str
    redis_stream_host: str
    redis_stream_port: int
    rest_api_server_url: str

    class Config:
        env_file = ".env"

settings = Settings()