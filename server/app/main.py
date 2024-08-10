from fastapi import FastAPI
from fastapi_pagination import add_pagination

from .auth.routers import router as user_router
from .routers import article_router, category_router, report_router

app = FastAPI()

app.include_router(user_router)
app.include_router(article_router)
app.include_router(category_router)
app.include_router(report_router)

add_pagination(app)
