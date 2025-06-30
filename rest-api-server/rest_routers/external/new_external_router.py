from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.params import Query
from sqlalchemy.ext.asyncio import AsyncSession

from common.base_response import BaseResponse
from rest_config.rest_api_db_session import get_db_session
from rest_depends.auth_depends import get_user_session
from rest_schemas.news_request_schema import SaveNewsRequest
from rest_schemas.user_schema import UserSession
from rest_services.news_service import NewsService

news_external_router = APIRouter(
    prefix="/news",
    tags=["externalNews"]
)

@news_external_router.post("/")
async def save_user_profile(
        request: SaveNewsRequest,
        user_session: UserSession = Depends(get_user_session),
        news_service: NewsService = Depends(NewsService),
        db: AsyncSession = Depends(get_db_session)
):
    return BaseResponse(
        status= 200,
        message="뉴스 추가 성공",
        data= await news_service.add_news(request, db, user_session)
    )

@news_external_router.get("/all")
async def get_all_news(
        page: int = Query(1, ge=1, description="페이지 번호 (1부터 시작)"),
        size: int = Query(10, ge=1, le=100, description="페이지 크기"),
        db: AsyncSession = Depends(get_db_session),
        news_service: NewsService = Depends(NewsService)
):
    return BaseResponse(
    status= 200,
    message="조회 성공",
    data = await news_service.find_all_news(db_session=db,page=page,size=size)
)

@news_external_router.get("/{id}")
async def get_news_by_id(
        news_id: UUID,
        db: AsyncSession = Depends(get_db_session),
        news_service: NewsService = Depends(NewsService)
):
    return BaseResponse(
        status= 200,
        message="조회 성공",
        data = await news_service.find_news_by_id(news_id=news_id, db_session= db, )
    )