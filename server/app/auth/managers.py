from fastapi_users import BaseUserManager, IntegerIDMixin

from .models import User
from app.settings import settings


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.JWT_SECRET
    verification_token_secret = settings.JWT_SECRET
