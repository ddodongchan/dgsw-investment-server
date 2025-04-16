from auth_repositories.user_credentials_repository import UserCredentialRepository
from auth_services.auth_service import AuthService


class AuthServiceDepends:
    def __init__(self):
        self.repo = UserCredentialRepository()
        self.service = AuthService(self.repo)

    def __call__(self) -> AuthService:
        return self.service