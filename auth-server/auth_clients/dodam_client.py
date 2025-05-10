import httpx
from auth_config.setting import Settings
from auth_schemas.dauth_schema import DauthLoginData, DauthLoginResponse, DauthTokenData, DauthUserData, DauthUserResponse
from auth_utils.ParameterExtractor import extract_code_from_location

settings = Settings()
async def __request_login_to_dauth(login_id: str, password: str) -> DauthLoginData:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://dauth.b1nd.com/api/auth/login",
            json={
                "id": login_id,
                "pw": password,
                "clientId": settings.dauth_client_id,
                "redirectUrl": settings.dauth_redirect_url,
                "state": None
            },
        )
        response.raise_for_status()
        parsed = DauthLoginResponse.model_validate(response.json())
        return parsed.data

async def __request_get_token(login_id: str, password: str) -> DauthTokenData:
    dauth_login_data: DauthLoginData = await __request_login_to_dauth(login_id, password)
    code = extract_code_from_location(dauth_login_data.location)
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://dauth.b1nd.com/api/token",
            json={
                "code": code,
                "client_id": settings.dauth_client_id,
                "client_secret": settings.dauth_client_secret,
            },
        )
        response.raise_for_status()
        return DauthTokenData.model_validate(response.json())


async def request_get_user(login_id: str, password: str) -> DauthUserData:
    dauth_token: DauthTokenData = await __request_get_token(login_id, password)
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://opendodam.b1nd.com/api/user",
            headers={"Authorization": f"Bearer {dauth_token.access_token}"},
        )
        response.raise_for_status()
        parsed = DauthUserResponse.model_validate(response.json())
        return parsed.data
