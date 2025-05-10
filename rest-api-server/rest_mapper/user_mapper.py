from functools import singledispatchmethod, singledispatch

from rest_models.user import User
from rest_schemas.user import UserCreate, UserRead


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
    def _(self, user_base: UserCreate) -> User:
        return User(
            login_id = user_base.login_id,
            role=user_base.role,
            status=user_base.status,
            email=str(user_base.email),
            name=user_base.name,
            profile_img=user_base.profile_img,
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