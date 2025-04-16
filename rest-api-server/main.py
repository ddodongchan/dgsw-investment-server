from fastapi import FastAPI

from rest_routers.internal.user_internal_router import user_internal_router

app = FastAPI()

app.include_router(user_internal_router)

@app.get("/")
async def root():
    return {"message": "Rest API Server is running 🚀"}
