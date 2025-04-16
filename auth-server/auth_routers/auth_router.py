from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth_config.db_session import get_db_session
from auth_depends.auth_depends import AuthServiceDepends
from auth_schemas.auth_request_schema import LoginRequest
from auth_schemas.auth_response_schema import Token
from auth_services.auth_service import AuthService
from base_response import BaseResponse

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=BaseResponse[Token])
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