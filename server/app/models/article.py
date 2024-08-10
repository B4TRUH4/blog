from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from ..models import Base


class Article(Base):
    """Таблица статей"""
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    author = relationship("User", back_populates="articles")
    category = relationship(
        "Category",
        back_populates="articles",
        lazy="joined"
    )
    comments = relationship(
        "Comment",
        back_populates="article",
        cascade="all, delete-orphan"
    )
    reports = relationship("Report", back_populates="article")
    reviews = relationship("Review", back_populates="article")
