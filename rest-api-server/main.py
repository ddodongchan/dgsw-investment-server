import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from rest_config.db_session import init_db, engine
from rest_models.base import Base
from rest_routers.external.news_external_router import news_external_router
from rest_routers.internal.user_internal_router import user_internal_router


# 모델들이 모두 초기화된 후에 테이블을 생성하도록 하는 코드
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# FastAPI lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Lifespan: Initializing DB and creating tables.")

    # 데이터베이스 초기화 및 테이블 생성
    await init_db()
    await create_tables()  # 테이블 생성 호출

    yield  # FastAPI 앱 실행 후 종료 시 처리될 코드


app = FastAPI(lifespan=lifespan)  # lifespan 컨텍스트 매니저 사용

# 라우터 등록
app.include_router(user_internal_router)
app.include_router(news_external_router)


@app.get("/")
async def root():
    return {"message": "Rest API Server is running 🚀"}