import asyncio
import math
from datetime import datetime, timezone
from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from pe_service.news_analyzer import NewsAnalyzer
from rest_clients.redis_client import get_redis
from rest_mapper.news_mapper import NewsMapper
from rest_mapper.stock_mapper import StockMapper
from rest_models.stock import Stock
from rest_repositories.news_repository import NewsRepository
from rest_repositories.stock_repository import StockRepository


class PeService:
    def __init__(
        self,
        stock_repository: StockRepository,
        news_repository: NewsRepository,
        news_analyzer: NewsAnalyzer,
        stock_mapper: StockMapper,
        news_mapper: NewsMapper,
    ):
        self.stock_repository = stock_repository
        self.news_repository = news_repository
        self.news_analyzer = news_analyzer
        self.stock_mapper = stock_mapper
        self.news_mapper = news_mapper

    async def change_price(self, db_session: AsyncSession) -> None:
        """모든 주식에 대해 가격을 갱신"""
        stocks: List[Stock] = await self.stock_repository.find_all(db_session)
        for stock in stocks:
            await self.calculate_price(stock.id, db_session)

    async def calculate_price(self, stock_id: UUID, db_session: AsyncSession) -> None:
        redis = await get_redis()

        # 1) 최근 3일 뉴스 조회
        news_list = await self.news_repository.find_by_date(
            stock_id=stock_id,
            days=3,
            db_session=db_session,
        )
        if not news_list:
            return

        # 2) 뉴스 스키마 변환
        news_schemas = [self.news_mapper.to_schema(news) for news in news_list]

        # 3) 병렬 감정 분석
        sentiments = await asyncio.gather(
            *(self.news_analyzer.analyze_sentiment(n.context) for n in news_schemas)
        )

        # 4) 점수 계산
        normalized_score = self._calculate_news_score(news_schemas, sentiments)

        # 5) 현재 주식 정보 조회
        stock = await self.stock_repository.find_by_id(stock_id, db_session)
        if not stock:
            raise ValueError(f"Stock not found: {stock_id}")

        # 6) 새 가격 계산
        new_price = self._calculate_new_price(stock, normalized_score)

        # 7) 주문 스트림에 추가
        order = {
            "user_id": UUID("98b3194d-a635-41b3-a6a6-093bd8aa1e95"),
            "type": "sell",
            "stock_code": stock_id,
            "amount": 3,
            "price": new_price,
            "timestamp": datetime.now(timezone.utc),
        }
        redis.xadd("order_stream", order)

    def _calculate_news_score(self, news_schemas, sentiments) -> float:
        """뉴스 리스트와 감정 리스트를 바탕으로 정규화된 점수 계산"""
        now = datetime.now(timezone.utc)
        total_score = 0.0

        for schema, sentiment in zip(news_schemas, sentiments):
            elapsed_hours = (now - schema.created_at).total_seconds() / 3600
            time_weight = max(1 - (elapsed_hours / 72), 0)  # 72시간 감쇠

            sentiment_score = {"positive": 1, "negative": -1}.get(sentiment, 0)
            total_score += sentiment_score * time_weight

        return total_score / max(len(news_schemas), 10)

    def _calculate_new_price(self, stock: Stock, normalized_score: float) -> float:
        """정규화된 점수 기반으로 새로운 주가 계산"""
        base_price = stock.current_price
        volume_weight = math.log((stock.volume or 0) + 1)
        volatility = 0.05  # 변동폭 5%

        delta = base_price * normalized_score * volatility * volume_weight
        return round(base_price + delta, 2)