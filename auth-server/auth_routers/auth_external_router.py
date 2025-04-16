from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from auth_config.db_session import get_db_session
from auth_depends.auth_depends import AuthServiceDepends
from auth_schemas.auth_request_schema import LoginRequest, TokenRefreshRequest
from auth_schemas.auth_response_schema import Token, AccessToken
from auth_services.auth_service import AuthService
from base_response import BaseResponse

auth_external_router = APIRouter(prefix="/auth", tags=["AuthExternal"])

@auth_external_router.post("/login", response_model=BaseResponse[Token])
async def login(
        request: LoginRequest,
        db: AsyncSession = Depends(get_db_session),
        auth_service: AuthService = Depends(AuthServiceDepends)
) -> BaseResponse[Token]:
    return BaseResponse(
        status= 200,
        message= "로그인 성공",
        data= await auth_service.login(
            request=request,
            db_session=db
        )
    )

@auth_external_router.post("/refresh", response_model=BaseResponse[AccessToken])
async def refresh(
        request: TokenRefreshRequest,
        db: AsyncSession = Depends(get_db_session),
        auth_service: AuthService = Depends(AuthServiceDepends)
) -> BaseResponse[AccessToken]:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing refresh token")

    token = auth_header.split(" ")[1]
    return BaseResponse(
        status= 200,
        message= "토큰 재발급 성공",
        data= await auth_service.refresh_token(token, db)
    )