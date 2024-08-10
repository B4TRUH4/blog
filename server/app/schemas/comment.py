from pydantic import BaseModel


class CommentBase(BaseModel):
    content: str


class CommentRead(CommentBase):
    id: int
    author_id: int


class CommentCreate(CommentBase):
    pass


class CommentUpdate(CommentBase):
    content: str | None = None
