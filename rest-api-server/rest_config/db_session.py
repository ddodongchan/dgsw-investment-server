from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from rest_config.setting import settings
from rest_models.base import Base

engine = create_async_engine(settings.database_url, echo=True)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

@asynccontextmanager
async def get_db_session_for_consumer() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        try:
            yield session  # 세션을 제공
            await session.commit()  # 커밋을 여기서 처리
        except Exception as e:
            await session.rollback()  # 롤백
            raise e  # 예외를 다시 던져서 상위 처리로 넘김
        finally:
            await session.close()  # 세션 종료

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        try:
            yield session  # 세션을 제공
            await session.commit()  # 커밋을 여기서 처리
        except Exception as e:
            await session.rollback()  # 롤백
            raise e  # 예외를 다시 던져서 상위 처리로 넘김
        finally:
            await session.close()  # 세션 종료

# 비동기 방식으로 테이블 생성
async def init_db():
    async with engine.begin() as conn:  # 연결 시작
        await conn.run_sync(Base.metadata.create_all)  # 테이블 생성
