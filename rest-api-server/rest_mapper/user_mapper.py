from functools import singledispatchmethod

from rest_models.user_profiles import UserProfile
from rest_schemas.user_request_schema import SaveUserProfileRequest

class UserMapper:
    @staticmethod
    @singledispatchmethod
    def to_model(request):
        raise NotImplementedError(f"지원하지 않는 타입: {type(request)}")

    @staticmethod
    @to_model.register
    def _(request: SaveUserProfileRequest) -> UserProfile:
        return UserProfile(
            user_credential_id=request.credential_id,
            email=request.email,
            name=request.name,
            profile_img=request.profile_image
        )