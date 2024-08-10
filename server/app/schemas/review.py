from pydantic import BaseModel, conint

from ..auth.schemas import UserRead


class ReviewBase(BaseModel):
    score: conint(ge=1, le=5)
    content: str | None = None


class ReviewRead(ReviewBase):
    id: int
    author: UserRead


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(ReviewBase):
    score: conint(ge=1, le=5) | None = None
