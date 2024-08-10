from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Integer, Column
from sqlalchemy.orm import relationship

from app.models.base import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    """Таблица пользователей"""
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)

    articles = relationship("Article", back_populates="author")
    comments = relationship("Comment", back_populates="author")
    reports = relationship("Report", back_populates="author")
