from pydantic import BaseModel, HttpUrl

class DauthLoginData(BaseModel):
    name: str
    profile_image: HttpUrl
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
    profile_image: HttpUrl
    role: str
    email: str

class DauthUserResponse(BaseModel):
    status: int
    message: str
    data: DauthUserData
