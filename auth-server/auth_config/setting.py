from pydantic import BaseSettings

class Settings(BaseSettings):
    dauth_client_id: str
    dauth_client_secret: str
    dauth_redirect_url: str
    internal_api_key: str
    database_url: str
    rest_api_server_url: str
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_access_expiration_time: int
    jwt_refresh_expiration_time: int

    class Config:
        env_file = "auth-server/.env"

settings = Settings()