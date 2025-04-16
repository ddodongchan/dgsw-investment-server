from sqlalchemy.ext.asyncio import AsyncSession

from auth_clients.dodam_client import request_get_user
from auth_clients.user_internal_api_client import request_save_user_profile
from auth_mapper.UserMapper import UserMapper
from auth_models.user_credentials import UserRole, UserStatus, UserCredential
from auth_repositories.user_credentials_repository import UserCredentialRepository
from auth_schemas.auth_request_schema import LoginRequest
from auth_schemas.auth_response_schema import Token
from auth_schemas.dauth_schema import DauthUserData
from auth_services.jwt_service import issue_token


class AuthService:
    def __init__(self, user_credential_repository: UserCredentialRepository):
        self.user_credential_repository = user_credential_repository

    async def login(self, request: LoginRequest, db_session: AsyncSession) -> Token:
        dauth_user: DauthUserData = await request_get_user(request.login_id, request.password)
        user = await self.user_credential_repository.find_by_login_id(dauth_user.uniqueId, db_session)
        if user is None:
            user = await self.__save_user(dauth_user, db_session)
        return issue_token(
            user_credential_id= user.id,
            role= user.role
        )

    async def __save_user(self, dauth_user: DauthUserData, db_session: AsyncSession) -> UserCredential:
        user_credential = UserCredential(
            login_id=dauth_user.uniqueId,
            role=UserRole.USER,
            status=UserStatus.ACTIVATE
        )
        db_session.add(user_credential)
        await request_save_user_profile(
            dauth_user.email,
            dauth_user.name,
            str(dauth_user.profile_image),
            user_credential.id
        )
        return user_credential