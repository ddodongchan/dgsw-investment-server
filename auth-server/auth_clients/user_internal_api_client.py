import httpx

from auth_config.setting import settings
from auth_schemas.user import UserCreate, UserRead


async def request_save_user_profile(user_create: UserCreate) -> UserRead:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.rest_api_server_url}/internal/users/",
            json= user_create.model_dump(),
            headers={"X-Internal-API-Key": f"{settings.internal_api_key}"},
        )
        response.raise_for_status()
        return UserRead(**response.json())

async def request_get_user_by_login_id(login_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.rest_api_server_url}/internal/users",
            headers={"X-Internal-API-Key": f"{settings.internal_api_key}"},
            params={"login_id": login_id}
        )
        response.raise_for_status()
        UserCreate.model_validate(response.json())
        return UserCreate(**response.json())