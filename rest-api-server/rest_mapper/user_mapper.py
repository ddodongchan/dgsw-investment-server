from functools import singledispatchmethod

from rest_models.user import User
from rest_schemas.user import UserRead, UserCreate


class UserMapper:
    def __init__(self):
        pass

    @singledispatchmethod
    def to_model(self, data, *args, **kwargs) -> User:
        raise NotImplementedError("지원하지 않는 타입입니다.")

    @singledispatchmethod
    def to_schema(self, data, *args, **kwargs) -> User:
        raise NotImplementedError("지원하지 않는 타입입니다.")

    @to_model.register
    def _(self, request: UserCreate) -> User:
        return User(
            login_id=request.login_id,
            email=request.email,
            name=request.name,
            status=request.status,
            role=request.role,
            profile_img=request.profile_image
        )

    @to_schema.register
    def _(self, user: User) -> UserRead :
        return UserRead(
            id=user.id,
            login_id=user.login_id,
            role=user.role,
            status=user.status,
            email=user.email,
            name=user.name,
            profile_img=user.profile_img
        )