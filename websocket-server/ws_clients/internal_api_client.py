import httpx
from pydantic import TypeAdapter

from ws_config.setting import settings
from ws_schemas.stock import Stock

async def request_get_stocks():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            settings.rest_api_server_url+"/stocks",
            headers={"X-Internal-API-Key": f"{settings.internal_api_key}"},
        )
        response.raise_for_status()
        adapter = TypeAdapter(list[Stock])
        return adapter.validate_python(response.json())