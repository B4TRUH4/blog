from sqlalchemy import Column, Integer, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship

from app.models import Base


class Review(Base):
    """Таблица отзыва на статью"""
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, index=True)
    score = Column(Integer, nullable=False)
    content = Column(Text,)
    article_id = Column(Integer, ForeignKey('articles.id'), nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    author = relationship("User", back_populates="reviews")
    article = relationship("Article", back_populates="reviews")
