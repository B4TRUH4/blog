from fastapi import FastAPI
from .auth.routers import router as user_router
from .routers import article_router, category_router

app = FastAPI()

app.include_router(user_router)
app.include_router(article_router)
app.include_router(category_router)
