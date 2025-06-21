import asyncio
import math
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from pe_service.news_analyzer import NewsAnalyzer
from rest_mapper.news_mapper import NewsMapper
from rest_repositories.news_repository import NewsRepository
from rest_repositories.stock_repository import StockRepository


class PeService:
    def __init__(self, stock_repository: StockRepository, news_repository: NewsRepository, news_analyzer: NewsAnalyzer, news_mapper: NewsMapper):
        self.stock_repository = stock_repository
        self.news_repository = news_repository
        self.news_analyzer = news_analyzer
        self.news_mapper = news_mapper

    async def calculate_price(self, stock_id: UUID, db_session: AsyncSession):
        # 3일간 뉴스 가져오기
        news_list = await self.news_repository.find_by_date(
            stock_id=stock_id, days=3, db_session=db_session
        )
        if not news_list:
            return  # 뉴스 없으면 종료

        # 스키마 변환
        schemas = [self.news_mapper.to_schema(news) for news in news_list]

        # 감정 분석 (병렬 처리)
        sentiment_tasks = [
            self.news_analyzer.analyze_sentiment(schema.context)
            for schema in schemas
        ]
        sentiments = await asyncio.gather(*sentiment_tasks)

        now = datetime.now(timezone.utc)

        # 뉴스별 점수 계산
        total_score = 0
        for schema, sentiment in zip(schemas, sentiments):
            # 시간 감쇠 계산
            elapsed = (now - schema.created_at).total_seconds() / 3600  # 시간 단위
            time_weight = max(1 - (elapsed / 72), 0)  # 72시간 이후 영향 없음

            # 감정 점수
            if sentiment == "positive":
                score = 1
            elif sentiment == "negative":
                score = -1
            else:
                score = 0

            total_score += score * time_weight

        # 뉴스 수 보정 (최대 10개로 정규화)
        normalized_score = total_score / max(len(schemas), 10)

        # 주식 정보 가져오기
        stock = await self.stock_repository.find_by_id(stock_id, db_session)
        if not stock:
            raise ValueError("Stock not found")

        base_price = stock.current_price
        volume = stock.volume or 1  # 거래량 (0 방지)
        volatility = 0.05  # 최대 변동폭 (5%)

        # 거래량에 따른 가중치 (로그 보정)
        volume_weight = math.log(volume + 1)

        # 최종 가격 계산
        delta = base_price * normalized_score * volatility * volume_weight
        new_price = round(base_price + delta, 2)

        # 저장
        stock.price = new_price
        await self.stock_repository.update(stock, db_session)