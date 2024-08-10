from sqlalchemy import Column, Integer, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship

from ..models import Base


class Report(Base):
    """Таблица жалобы на статью"""
    __tablename__ = 'reports'
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text,)
    article_id = Column(Integer, ForeignKey('articles.id'), nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    solved = Column(Boolean, default=False, nullable=False)

    author = relationship("User", back_populates="reports")
    article = relationship("Article", back_populates="reports")
