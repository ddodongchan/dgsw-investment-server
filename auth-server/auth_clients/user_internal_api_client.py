from uuid import UUID

import httpx

from auth_config.setting import settings

async def request_save_user_profile(email: str, name: str, profile_image: str, credential_id: UUID):
    async with httpx.AsyncClient() as client:
        await client.post(
            f"{settings.rest_api_server_url}/users",
            json= {
                email: email,
                name: name,
                profile_image: profile_image,
                credential_id: credential_id
            },
            headers={"X-Internal-API-Key": f"{settings.internal_api_key}"},
        )