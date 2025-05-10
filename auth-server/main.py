from fastapi import FastAPI

from auth_routers.auth_external_router import auth_external_router
from auth_routers.auth_internal_router import auth_internal_router


# FastAPI 앱 생성
app = FastAPI()


app.include_router(auth_external_router)
app.include_router(auth_internal_router, prefix="/internal")
