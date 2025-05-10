from rest_mapper.user_mapper import UserMapper
from rest_repositories.user_repository import UserRepository
from rest_services.user_service import UserService

class UserServiceDepends:
    def __init__(self):
        self.user_repository = UserRepository()
        self.user_mapper = UserMapper()

    def __call__(self) -> UserService:
        return UserService(
            user_repository=self.user_repository,
            user_mapper=self.user_mapper
        )
