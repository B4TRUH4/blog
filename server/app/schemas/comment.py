from pydantic import BaseModel

from ..auth.schemas import UserRead


class CommentBase(BaseModel):
    content: str


class CommentRead(CommentBase):
    id: int
    author: UserRead


class CommentCreate(CommentBase):
    pass


class CommentUpdate(CommentBase):
    content: str | None = None
