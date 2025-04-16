from functools import singledispatchmethod

from rest_models.user_profiles import UserProfile
from rest_schemas.user_request_schema import SaveUserProfileRequest, UserProfileRequest


class UserMapper:
    @singledispatchmethod
    def to_model(self, request, *args, **kwargs) -> UserProfile:
        raise NotImplementedError("지원하지 않는 타입입니다.")

    @to_model.register
    def _(self, request: SaveUserProfileRequest) -> UserProfile:
        return UserProfile(
            user_credential_id=request.credential_id,
            email=request.email,
            name=request.name,
            profile_img=request.profile_image
        )
