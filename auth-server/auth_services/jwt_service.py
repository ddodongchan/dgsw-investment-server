from uuid import UUID

from fastapi import HTTPException, status
from jose import jwt, JWTError
from datetime import datetime, timedelta
from auth_config.setting import Settings, settings
from auth_schemas.auth_response_schema import Token


class JwtService:
    @staticmethod
    def issue_token(user_credential_id: UUID, role: str) -> Token:
        return Token(
            access_token=JwtService.create_access_token(user_credential_id, role),
            refresh_token=JwtService.create_refresh_token(user_credential_id)
        )

    @staticmethod
    def create_access_token(user_credential_id: UUID, role: str) -> str:
        payload = {
            "sub": user_credential_id,
            "role": role,
            "type": "access",
            "exp": datetime.now() + timedelta(minutes=settings.jwt_access_expiration_time)
        }
        return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

    @staticmethod
    def create_refresh_token(user_credential_id: UUID) -> str:
        payload = {
            "sub": user_credential_id,
            "type": "refresh",
            "exp": datetime.now() + timedelta(days=settings.jwt_refresh_expiration_time)
        }
        return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")