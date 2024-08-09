from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship

from .base import Base


class Category(Base):
    """Таблица категорий"""
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, unique=True, nullable=False)

    articles = relationship("Article", back_populates="category")
