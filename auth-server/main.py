from fastapi import FastAPI

from auth_routers.auth_router import auth_router

app = FastAPI()

app.include_router(auth_router)
