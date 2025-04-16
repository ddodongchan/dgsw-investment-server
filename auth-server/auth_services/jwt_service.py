from uuid import UUID

from jose import jwt, JWTError
from datetime import datetime, timedelta
from auth_config.setting import Settings
from auth_models.user_credentials import UserRole
from auth_schemas.auth_response_schema import Token


def issue_token(user_credential_id: UUID, role: UserRole) -> Token:
    return Token(
        access_token=create_access_token(user_credential_id, role),
        refresh_token=create_refresh_token(user_credential_id)
    )

def create_access_token(user_credential_id: UUID, role: UserRole) -> str:
    payload = {
        "sub": user_credential_id,
        "role": role.value,
        "type": "access",
        "exp": datetime.now() + timedelta(minutes=Settings.jwt_access_expiration_time)
    }
    return jwt.encode(payload, Settings.jwt_secret_key, algorithm=Settings.jwt_algorithm)

def create_refresh_token(user_credential_id: UUID) -> str:
    payload = {
        "sub": user_credential_id,
        "type": "refresh",
        "exp": datetime.now() + timedelta(days=Settings.jwt_refresh_expiration_time)
    }
    return jwt.encode(payload, Settings.jwt_secret_key, algorithm=Settings.jwt_algorithm)
