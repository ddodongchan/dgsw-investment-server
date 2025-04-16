from pydantic import BaseSettings

class Settings(BaseSettings):
    internal_api_key: str
    database_url: str

    class Config:
        env_file = "rest-api-server/.env"

settings = Settings()