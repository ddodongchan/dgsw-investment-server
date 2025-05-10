from typing import Optional

from pydantic import BaseModel, HttpUrl, EmailStr


class DauthLoginData(BaseModel):
    name: str
    profile_image: Optional[HttpUrl] = None
    location: HttpUrl

class DauthLoginResponse(BaseModel):
    status: int
    message: str
    data: DauthLoginData

class DauthTokenData(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: str

class DauthTokenResponse(BaseModel):
    status: int
    message: str
    data: DauthTokenData

class DauthUserData(BaseModel):
    uniqueId: str
    grade: int
    room: int
    number: int
    name: str
    profile_image: Optional[HttpUrl] = None
    role: str
    email: EmailStr

class DauthUserResponse(BaseModel):
    status: int
    message: str
    data: DauthUserData
