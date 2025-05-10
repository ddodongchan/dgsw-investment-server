from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from auth_clients.dodam_client import request_get_user
from auth_clients.user_internal_api_client import request_save_user_profile
from auth_schemas.auth_request_schema import LoginRequest
from auth_schemas.auth_response_schema import Token, AccessToken
from auth_schemas.dauth_schema import DauthUserData
from auth_schemas.user import UserCreate, UserRole, UserStatus
from auth_services.jwt_service import JwtService


class AuthService:
    def __init__(self):
        pass

    async def login(self, request: LoginRequest) -> Token:
        dauth_user: DauthUserData = await request_get_user(request.login_id, request.password)
        user = await request_save_user_profile(
            UserCreate(
                login_id=dauth_user.uniqueId,
                role=UserRole.USER,
                status=UserStatus.ACTIVATE,
                email=dauth_user.email,
                name=dauth_user.name,
                profile_img=dauth_user.profile_image,
            )
        )
        return JwtService.issue_token(
            id=user.id,
            role=user.role.value
        )

    async def refresh_token(self, token: str, db_session: AsyncSession) -> AccessToken:
        payload = JwtService.decode_token(token)

        user_id = payload.get("sub")
        role = payload.get("role", "user")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        access_token = JwtService.create_access_token(id=user_id, role=role)
        return AccessToken(access_token=access_token)

    async def validate_token(self, token: str):
        payload = JwtService.decode_token(token)
        user_id = payload.get("sub")
        role = payload.get("role")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return {
            "X-User-ID": user_id,
            "X-User-Role": role
        }