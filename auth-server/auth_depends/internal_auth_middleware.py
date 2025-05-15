from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyHeader

from rest_config.setting import settings

API_KEY = settings.internal_api_key
API_KEY_NAME = "X-Internal-API-Key"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def verify_internal_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key