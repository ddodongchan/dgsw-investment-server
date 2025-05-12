from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.params import Query
from sqlalchemy.ext.asyncio import AsyncSession

from rest_common.base_response import BaseResponse
from rest_config.db_session import get_db_session
from rest_depends.auth_depends import get_user_session
from rest_depends.news_depends import NewsServiceDepends
from rest_depends.user_depends import UserServiceDepends
from rest_repositories.news_repository import NewsRepository
from rest_repositories.user_repository import UserRepository
from rest_schemas.news_request_schema import SaveNewsRequest, UpdateNewsRequest
from rest_schemas.user_schema import UserSession
from rest_services.news_service import NewsService

news_external_router = APIRouter(
    prefix="/news",
    tags=["externalNews"]
)

def get_news_service(
    user_repo: UserRepository = Depends(UserServiceDepends()),
    news_repo: NewsRepository = Depends(NewsServiceDepends()),
) -> NewsService:
    return NewsService(user_repo, news_repo)

@news_external_router.post("/")
async def save_user_profile(
        request: SaveNewsRequest,
        user_session: UserSession = Depends(get_user_session),
        news_service: NewsService = Depends(NewsServiceDepends()),
        db: AsyncSession = Depends(get_db_session)
):
    await news_service.add_news(request, db, user_session)
    return BaseResponse(
        status= 200,
        message="뉴스 추가 성공",
    )

@news_external_router.get("/all")
async def get_all_news(
        page: int = Query(1, ge=1, description="페이지 번호 (1부터 시작)"),
        size: int = Query(10, ge=1, le=100, description="페이지 크기"),
        db: AsyncSession = Depends(get_db_session),
        news_service: NewsService = Depends(NewsServiceDepends()),
):
    return BaseResponse(
    status= 200,
    message="조회 성공",
    data = await news_service.find_all_news(db_session=db,page=page,size=size)
)

@news_external_router.get("/{news_id}")
async def get_news_by_id(
        news_id: UUID,
        db: AsyncSession = Depends(get_db_session),
        news_service: NewsService = Depends(NewsServiceDepends()),
):
    return BaseResponse(
        status= 200,
        message="조회 성공",
        data = await news_service.find_news_by_id(news_id=news_id, db_session= db, )
    )

@news_external_router.patch("/")
async def save_user_profile(
        request: UpdateNewsRequest,
        user_session: UserSession = Depends(get_user_session),
        news_service: NewsService = Depends(NewsServiceDepends()),
        db: AsyncSession = Depends(get_db_session)
):
    await news_service.update_news(
        request=request, db_session=db, user_session=user_session)
    return BaseResponse(
        status= 200,
        message="뉴스 수정 성공",
    )