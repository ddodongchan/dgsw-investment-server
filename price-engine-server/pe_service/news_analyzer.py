import openai
from fastapi import HTTPException

from pe_config.setting import settings


class NewsAnalyzer:
    def __init__(self):
        pass

    openai.api_key = settings.openai_key

    @staticmethod
    async def analyze_sentiment(content : str):
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "너는 감정 분석기야. 사용자가 제공하는 뉴스 본문이 긍정적인지 부정적인지 판단해서 "
                            "무조건 'positive' 또는 'negative' 중 하나의 단어만 출력해. "
                            "절대 다른 단어나 설명을 추가하지 마."
                        )
                    },
                    {"role": "user", "content": content}
                ],
                temperature=0.0,  # 정확도 우선
                max_tokens=1  # 결과는 한 단어
            )
            result = response.choices[0].message.content.strip().lower()
            if result not in ["positive", "negative"]:
                raise ValueError("Invalid response from model: " + result)
            return {"sentiment": result}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))