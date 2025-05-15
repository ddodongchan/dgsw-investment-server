from fastapi import FastAPI

from ws_router.websocket_router import websocket_router

app = FastAPI()

app.include_router(websocket_router)

@app.get("/")
async def root():
    return {"message": "Rest API Server is running 🚀"}
