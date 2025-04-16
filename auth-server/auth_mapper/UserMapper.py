from functools import singledispatchmethod

from auth_models.user_credentials import UserCredential, UserRole, UserStatus
from auth_schemas.dauth_schema import DauthUserData


class UserMapper:
    @staticmethod
    def to_model_from_dauth_user_data(data: DauthUserData, role: UserRole, status: UserStatus) -> UserCredential:
        return UserCredential(
            login_id = data.uniqueId,
            role = role,
            status = status
        )

