from auth_services.auth_service import AuthService

class AuthServiceDepends:
    def __init__(self):
        self.service = AuthService()

    def __call__(self) -> AuthService:
        return self.service