from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Integer, Column
from app.models.base import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
