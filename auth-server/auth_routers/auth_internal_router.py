from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse, Response

from auth_depends.auth_depends import AuthServiceDepends
from auth_services.auth_service import AuthService

auth_internal_router = APIRouter(prefix="/auth", tags=["AuthInternal"])

@auth_internal_router.get("/validate")
async def validate(
        request: Request,
        auth_service: AuthService = Depends(AuthServiceDepends)
):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content={"detail": "Missing or invalid token"})

    token = auth_header.split(" ")[1]
    return Response(headers= await auth_service.validate_token(token))