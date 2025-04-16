from pydantic import BaseModel

class LoginRequest(BaseModel):
    login_id: str
    password: str

class TokenRefreshRequest(BaseModel):
    refresh_token: str