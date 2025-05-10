from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar("T")

class BaseResponse(BaseModel, Generic[T]):
    status: int
    message: Optional[str] = None
    data: Optional[T] = None
