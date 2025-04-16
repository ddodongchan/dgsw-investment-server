from rest_repositories.user_profile_repository import UserProfileRepository
from rest_services.user_service import UserService


class UserServiceDepends:
    def __init__(self):
        self.service = UserService()

    def __call__(self) -> UserService:
        return self.service